"""Agno tools wrapping the WSI ingestion module."""

from __future__ import annotations

import json

from agno.tools.decorator import tool

from wsi_py_ai.backends.factory import get_backends
from wsi_py_ai.config.settings import WSIPipelineConfig
from wsi_py_ai.ingest.ingester import WSIIngester


@tool
def ingest_file(source_path: str, study_id: str) -> str:
    """Ingest a single WSI file into the pipeline.

    Args:
        source_path: Path to the WSI file (SVS, NDPI, DICOM, etc.).
        study_id: Study identifier to associate with this slide.

    Returns:
        JSON string with ingestion result (slide_id, status, metadata).
    """
    config = WSIPipelineConfig()
    backends = get_backends(config)
    ingester = WSIIngester(backends)
    result = ingester.ingest(source_path=source_path, study_id=study_id)
    return json.dumps(result.model_dump(), default=str)


@tool
def ingest_batch(source_dir: str, study_id: str, pattern: str = "*.svs") -> str:
    """Ingest all matching WSI files from a directory.

    Args:
        source_dir: Directory containing WSI files.
        study_id: Study identifier for all slides in this batch.
        pattern: Glob pattern for matching files (default: *.svs).

    Returns:
        JSON string with list of ingestion results.
    """
    config = WSIPipelineConfig()
    backends = get_backends(config)
    ingester = WSIIngester(backends)
    results = ingester.batch_ingest(source_dir=source_dir, study_id=study_id, pattern=pattern)
    return json.dumps([r.model_dump() for r in results], default=str)
