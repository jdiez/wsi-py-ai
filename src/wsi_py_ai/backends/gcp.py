"""GCP cloud backend implementations.

Requires the 'gcp' optional dependency group:
    uv add --group gcp google-cloud-storage google-cloud-bigquery ...
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

from wsi_py_ai.backends.base import ComputeBackend, InferenceBackend, RegistryBackend, StorageBackend


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
        self.project_id = project_id
        self.bucket_name = bucket_name

    def upload(self, local_path: Path, remote_key: str) -> str:
        """Upload file to GCS.

        Args:
            local_path: Local file to upload.
            remote_key: GCS object key.

        Returns:
            GCS URI (gs://bucket/key).

        Raises:
            NotImplementedError: Requires google-cloud-storage.
        """
        raise NotImplementedError("GCS backend requires: uv add google-cloud-storage")

    def download(self, remote_key: str, local_path: Path) -> Path:
        """Download file from GCS.

        Args:
            remote_key: GCS object key.
            local_path: Local destination.

        Returns:
            Local path of downloaded file.

        Raises:
            NotImplementedError: Requires google-cloud-storage.
        """
        raise NotImplementedError("GCS backend requires: uv add google-cloud-storage")

    def list_files(self, prefix: str, pattern: str = "*") -> Iterator[str]:
        """List objects in GCS bucket.

        Args:
            prefix: Object prefix.
            pattern: Glob pattern (applied client-side).

        Yields:
            GCS object keys.

        Raises:
            NotImplementedError: Requires google-cloud-storage.
        """
        raise NotImplementedError("GCS backend requires: uv add google-cloud-storage")

    def exists(self, key: str) -> bool:
        """Check if object exists in GCS.

        Args:
            key: GCS object key.

        Returns:
            True if object exists.

        Raises:
            NotImplementedError: Requires google-cloud-storage.
        """
        raise NotImplementedError("GCS backend requires: uv add google-cloud-storage")


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
        self.project_id = project_id
        self.dataset = dataset

    def register_slide(self, slide_id: str, metadata: dict[str, Any]) -> None:
        """Register slide in BigQuery.

        Args:
            slide_id: Unique slide identifier.
            metadata: Slide metadata.

        Raises:
            NotImplementedError: Requires google-cloud-bigquery.
        """
        raise NotImplementedError("BigQuery backend requires: uv add google-cloud-bigquery")

    def query(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        """Query slides from BigQuery.

        Args:
            filters: Query filters.

        Returns:
            Matching slide records.

        Raises:
            NotImplementedError: Requires google-cloud-bigquery.
        """
        raise NotImplementedError("BigQuery backend requires: uv add google-cloud-bigquery")

    def update(self, slide_id: str, fields: dict[str, Any]) -> None:
        """Update slide record in BigQuery.

        Args:
            slide_id: Slide to update.
            fields: Fields to update.

        Raises:
            NotImplementedError: Requires google-cloud-bigquery.
        """
        raise NotImplementedError("BigQuery backend requires: uv add google-cloud-bigquery")


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
        """Run batch processing via Dataflow.

        Args:
            fn: Processing function.
            items: Items to process.
            max_workers: Max Dataflow workers.

        Returns:
            Processing results.

        Raises:
            NotImplementedError: Requires apache-beam[gcp].
        """
        raise NotImplementedError("Dataflow backend requires: uv add 'apache-beam[gcp]'")


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
        self.project_id = project_id
        self.endpoint = endpoint

    def predict(self, model_name: str, inputs: list[Any]) -> list[Any]:
        """Run batch prediction via Vertex AI.

        Args:
            model_name: Model name (used for routing).
            inputs: Prediction inputs.

        Returns:
            Prediction results.

        Raises:
            NotImplementedError: Requires google-cloud-aiplatform.
        """
        raise NotImplementedError("Vertex backend requires: uv add google-cloud-aiplatform")
