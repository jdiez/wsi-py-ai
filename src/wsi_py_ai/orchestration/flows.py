"""Prefect flow definitions for WSI pipeline orchestration.

Requires the 'orchestration-prefect' optional dependency group:
    pip install wsi-py-ai[orchestration-prefect]
"""

from __future__ import annotations

from typing import Any

from prefect import flow, task

from wsi_py_ai.backends.factory import get_backends
from wsi_py_ai.config.settings import WSIPipelineConfig


@task(name="wsi-ingest", retries=3, retry_delay_seconds=30)
def ingest_task(
    source_dir: str,
    study_id: str,
    pattern: str = "*",
    parallelism: int = 4,
) -> list[dict[str, Any]]:
    """Ingest WSI files as a Prefect task with automatic retries.

    Args:
        source_dir: Directory containing WSI files.
        study_id: Study identifier.
        pattern: Glob pattern for file matching.
        parallelism: Number of parallel workers.

    Returns:
        List of serialized IngestResult dicts.
    """
    from wsi_py_ai.ingest.ingester import WSIIngester

    config = WSIPipelineConfig()
    backends = get_backends(config)
    ingester = WSIIngester(backends)
    results = ingester.batch_ingest(source_dir, study_id, pattern=pattern, parallelism=parallelism)
    return [r.model_dump() for r in results]


@task(name="wsi-deid", retries=2, retry_delay_seconds=60)
def deid_task(study_id: str) -> list[dict[str, Any]]:
    """De-identify all slides in a study as a Prefect task.

    Args:
        study_id: Study identifier.

    Returns:
        List of serialized DeidResult dicts.
    """
    from wsi_py_ai.deid.deidentifier import WSIDeidentifier

    config = WSIPipelineConfig()
    backends = get_backends(config)
    deidentifier = WSIDeidentifier(backends)
    results = deidentifier.batch_deidentify(study_id)
    return [r.model_dump() for r in results]


@task(name="wsi-qa", retries=2, retry_delay_seconds=30)
def qa_task(study_id: str) -> list[dict[str, Any]]:
    """Run QA assessment on all slides in a study as a Prefect task.

    Args:
        study_id: Study identifier.

    Returns:
        List of serialized QAReport dicts.
    """
    from wsi_py_ai.qa.runner import QARunner

    config = WSIPipelineConfig()
    backends = get_backends(config)
    runner = QARunner(backends)
    reports = runner.batch_assess(study_id)
    return [r.model_dump() for r in reports]


@flow(name="wsi-pipeline", log_prints=True)
def wsi_pipeline_flow(
    source_dir: str,
    study_id: str,
    pattern: str = "*",
    parallelism: int = 4,
    skip_deid: bool = False,
) -> dict[str, Any]:
    """End-to-end WSI pipeline as a Prefect flow.

    Orchestrates: ingest -> de-identify -> QA assessment.
    Each step is a separate Prefect task with retry logic.

    Args:
        source_dir: Directory containing WSI files.
        study_id: Study identifier.
        pattern: Glob pattern for file matching.
        parallelism: Parallel workers for ingestion.
        skip_deid: Skip de-identification (DANGEROUS — for testing only).

    Returns:
        Summary dict with counts and results.
    """
    print(f"Starting WSI pipeline for study {study_id}")

    ingest_results = ingest_task(source_dir, study_id, pattern, parallelism)
    print(f"Ingested {len(ingest_results)} slides")

    deid_results: list[dict[str, Any]] = []
    if not skip_deid:
        deid_results = deid_task(study_id)
        print(f"De-identified {len(deid_results)} slides")
    else:
        print("WARNING: De-identification skipped")

    qa_results = qa_task(study_id)
    passed = sum(1 for r in qa_results if r.get("passed"))
    print(f"QA: {passed}/{len(qa_results)} passed")

    return {
        "study_id": study_id,
        "ingested": len(ingest_results),
        "deidentified": len(deid_results),
        "qa_passed": passed,
        "qa_total": len(qa_results),
    }
