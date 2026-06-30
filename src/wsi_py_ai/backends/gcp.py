"""GCP cloud backend implementations.

Requires the 'gcp' optional dependency group:
    pip install wsi-py-ai[gcp]
"""

from __future__ import annotations

import fnmatch
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import structlog

from wsi_py_ai.backends.base import ComputeBackend, InferenceBackend, RegistryBackend, StorageBackend

logger: structlog.stdlib.BoundLogger = structlog.get_logger("wsi_py_ai.backends.gcp")


class GCSStorageBackend(StorageBackend):
    """Google Cloud Storage backend.

    Attributes:
        project_id: GCP project ID.
        bucket_name: Default GCS bucket name.
    """

    def __init__(self, project_id: str, bucket_name: str) -> None:
        """Initialize GCS storage backend.

        Args:
            project_id: GCP project identifier.
            bucket_name: GCS bucket name for storage.
        """
        from google.cloud import storage

        self.project_id = project_id
        self.bucket_name = bucket_name
        self._client = storage.Client(project=project_id)
        self._bucket = self._client.bucket(bucket_name)

    def upload(self, local_path: Path, remote_key: str) -> str:
        """Upload file to GCS.

        Args:
            local_path: Local file to upload.
            remote_key: GCS object key.

        Returns:
            GCS URI (gs://bucket/key).
        """
        blob = self._bucket.blob(remote_key)
        blob.upload_from_filename(str(local_path))
        uri = f"gs://{self.bucket_name}/{remote_key}"
        logger.info("gcs.uploaded", uri=uri, size=local_path.stat().st_size)
        return uri

    def download(self, remote_key: str, local_path: Path) -> Path:
        """Download file from GCS.

        Args:
            remote_key: GCS object key.
            local_path: Local destination.

        Returns:
            Local path of downloaded file.
        """
        blob = self._bucket.blob(remote_key)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(str(local_path))
        logger.info("gcs.downloaded", key=remote_key, dest=str(local_path))
        return local_path

    def list_files(self, prefix: str, pattern: str = "*") -> Iterator[str]:
        """List objects in GCS bucket.

        Args:
            prefix: Object prefix to filter by.
            pattern: Glob pattern (applied client-side to blob names).

        Yields:
            GCS object keys matching prefix and pattern.
        """
        blobs = self._client.list_blobs(self._bucket, prefix=prefix)
        for blob in blobs:
            name: str = blob.name
            basename = name.rsplit("/", 1)[-1] if "/" in name else name
            if fnmatch.fnmatch(basename, pattern):
                yield name

    def exists(self, key: str) -> bool:
        """Check if object exists in GCS.

        Args:
            key: GCS object key.

        Returns:
            True if object exists.
        """
        blob = self._bucket.blob(key)
        return bool(blob.exists())


class BigQueryRegistryBackend(RegistryBackend):
    """BigQuery-based registry backend for cloud-scale metadata.

    Attributes:
        project_id: GCP project ID.
        dataset: BigQuery dataset name.
    """

    def __init__(self, project_id: str, dataset: str) -> None:
        """Initialize BigQuery registry.

        Args:
            project_id: GCP project identifier.
            dataset: BigQuery dataset containing the slides table.
        """
        from google.cloud import bigquery

        self.project_id = project_id
        self.dataset = dataset
        self._client = bigquery.Client(project=project_id)
        self._table_id = f"{project_id}.{dataset}.slides"

    def register_slide(self, slide_id: str, metadata: dict[str, Any]) -> None:
        """Register slide in BigQuery.

        Args:
            slide_id: Unique slide identifier.
            metadata: Slide metadata.
        """
        import json

        row = {"slide_id": slide_id, "metadata_json": json.dumps(metadata), **metadata}
        errors = self._client.insert_rows_json(self._table_id, [row])
        if errors:
            msg = f"BigQuery insert errors: {errors}"
            raise RuntimeError(msg)
        logger.info("bq.registered", slide_id=slide_id)

    def query(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        """Query slides from BigQuery.

        Args:
            filters: Query filters as key-value pairs.

        Returns:
            Matching slide records.
        """
        import json

        where_clauses = []
        params: list[Any] = []
        for key, value in filters.items():
            where_clauses.append(f"JSON_VALUE(metadata_json, '$.{key}') = @p{len(params)}")
            params.append(value)

        where_sql = " AND ".join(where_clauses) if where_clauses else "TRUE"
        query_str = f"SELECT slide_id, metadata_json FROM `{self._table_id}` WHERE {where_sql}"  # noqa: S608  # nosec B608 - parameterized via BigQuery ScalarQueryParameter

        from google.cloud import bigquery

        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter(f"p{i}", "STRING", str(v)) for i, v in enumerate(params)]
        )
        results = self._client.query(query_str, job_config=job_config)

        rows: list[dict[str, Any]] = []
        for row in results:
            meta: dict[str, Any] = json.loads(row["metadata_json"])
            rows.append({"slide_id": row["slide_id"], **meta})
        return rows

    def update(self, slide_id: str, fields: dict[str, Any]) -> None:
        """Update slide record in BigQuery.

        Merges new fields into existing metadata JSON.

        Args:
            slide_id: Slide to update.
            fields: Fields to merge.
        """
        import json

        existing = self.query({"slide_id": slide_id})
        if not existing:
            msg = f"Slide {slide_id} not found in BigQuery"
            raise ValueError(msg)

        merged = {**existing[0], **fields}
        merged.pop("slide_id", None)

        from google.cloud import bigquery

        query_str = (
            f"UPDATE `{self._table_id}` "  # noqa: S608  # nosec B608 - parameterized via BigQuery ScalarQueryParameter
            f"SET metadata_json = @metadata "
            f"WHERE slide_id = @slide_id"
        )
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("metadata", "STRING", json.dumps(merged)),
                bigquery.ScalarQueryParameter("slide_id", "STRING", slide_id),
            ]
        )
        self._client.query(query_str, job_config=job_config).result()
        logger.info("bq.updated", slide_id=slide_id, fields=list(fields.keys()))


class DataflowComputeBackend(ComputeBackend):
    """Dataflow (Apache Beam) compute backend.

    Attributes:
        project_id: GCP project ID.
        region: GCP region for Dataflow jobs.
    """

    def __init__(self, project_id: str, region: str) -> None:
        """Initialize Dataflow compute backend.

        Args:
            project_id: GCP project identifier.
            region: GCP region (e.g., us-central1).
        """
        self.project_id = project_id
        self.region = region

    def run_batch(self, fn: Any, items: list[Any], max_workers: int = 4) -> list[Any]:
        """Run batch processing via Apache Beam on Dataflow.

        Args:
            fn: Processing function to apply to each item.
            items: Items to process.
            max_workers: Max Dataflow workers.

        Returns:
            Processing results as a list.
        """
        import apache_beam as beam
        from apache_beam.options.pipeline_options import PipelineOptions

        options = PipelineOptions(
            runner="DataflowRunner",
            project=self.project_id,
            region=self.region,
            max_num_workers=max_workers,
            temp_location=f"gs://{self.project_id}-dataflow-temp/tmp",
        )

        results: list[Any] = []

        with beam.Pipeline(options=options) as pipeline:
            output = pipeline | "CreateItems" >> beam.Create(items) | "ProcessItems" >> beam.Map(fn)
            output | "Collect" >> beam.Map(results.append)

        logger.info("dataflow.completed", item_count=len(items), workers=max_workers)
        return results


class VertexInferenceBackend(InferenceBackend):
    """Vertex AI inference backend for batch predictions.

    Attributes:
        project_id: GCP project ID.
        endpoint: Vertex AI endpoint name.
    """

    def __init__(self, project_id: str, endpoint: str) -> None:
        """Initialize Vertex AI inference backend.

        Args:
            project_id: GCP project identifier.
            endpoint: Vertex AI endpoint resource name.
        """
        from google.cloud import aiplatform

        self.project_id = project_id
        self.endpoint_name = endpoint
        aiplatform.init(project=project_id)
        self._endpoint = aiplatform.Endpoint(endpoint)

    def predict(self, model_name: str, inputs: list[Any]) -> list[Any]:
        """Run batch prediction via Vertex AI endpoint.

        Args:
            model_name: Model name (for logging; endpoint is pre-configured).
            inputs: Prediction inputs (serializable to JSON).

        Returns:
            Prediction results from the endpoint.
        """
        response = self._endpoint.predict(instances=inputs)
        logger.info("vertex.predicted", model=model_name, count=len(inputs))
        return list(response.predictions)
