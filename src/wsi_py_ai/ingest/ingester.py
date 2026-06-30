"""WSI ingestion orchestrator."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

import structlog

from wsi_py_ai.core.types import IngestResult, SlideFormat, SlideMetadata

logger: structlog.stdlib.BoundLogger = structlog.get_logger("wsi_py_ai.ingest")

FORMAT_MAP: dict[str, SlideFormat] = {
    ".svs": SlideFormat.SVS,
    ".ndpi": SlideFormat.NDPI,
    ".dcm": SlideFormat.DICOM,
    ".isyntax": SlideFormat.ISYNTAX,
    ".mrxs": SlideFormat.MRXS,
    ".tif": SlideFormat.TIFF,
    ".tiff": SlideFormat.TIFF,
    ".bif": SlideFormat.BIF,
}


class WSIIngester:
    """Orchestrates WSI file ingestion into storage and registry.

    Attributes:
        backends: Dictionary of backend instances (storage, registry, compute).
    """

    def __init__(self, backends: dict[str, Any]) -> None:
        """Initialize ingester with backend instances.

        Args:
            backends: Backend dictionary from get_backends().
        """
        self.storage = backends["storage"]
        self.registry = backends["registry"]
        self.compute = backends["compute"]

    def ingest(
        self,
        source_path: str | Path,
        study_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> IngestResult:
        """Ingest a single WSI file.

        Args:
            source_path: Path to the source WSI file.
            study_id: Study identifier to associate with.
            metadata: Optional additional metadata.

        Returns:
            IngestResult with slide_id, storage URI, and metadata.

        Raises:
            FileNotFoundError: If source_path does not exist.
            ValueError: If file format is not supported.
        """
        path = Path(source_path)
        if not path.exists():
            msg = f"Source file not found: {source_path}"
            raise FileNotFoundError(msg)

        suffix = path.suffix.lower()
        if suffix not in FORMAT_MAP:
            msg = f"Unsupported format: {suffix}"
            raise ValueError(msg)

        slide_id = str(uuid4())
        slide_format = FORMAT_MAP[suffix]
        remote_key = f"raw/{study_id}/{slide_id}{suffix}"

        storage_uri = self.storage.upload(path, remote_key)

        slide_meta = SlideMetadata(
            slide_id=slide_id,
            study_id=study_id,
            format=slide_format,
            file_size_bytes=path.stat().st_size,
            **(metadata or {}),
        )

        self.registry.register_slide(slide_id, slide_meta.model_dump())
        logger.info("slide.ingested", slide_id=slide_id, study_id=study_id, format=slide_format.value)

        return IngestResult(slide_id=slide_id, storage_uri=storage_uri, metadata=slide_meta)

    def batch_ingest(
        self,
        source_dir: str | Path,
        study_id: str,
        pattern: str = "*",
        parallelism: int = 4,
    ) -> list[IngestResult]:
        """Ingest all matching WSI files from a directory.

        Args:
            source_dir: Directory containing WSI files.
            study_id: Study identifier.
            pattern: Glob pattern for file matching.
            parallelism: Number of parallel workers.

        Returns:
            List of IngestResults for each processed file.
        """
        dir_path = Path(source_dir)
        files = [f for f in dir_path.glob(pattern) if f.suffix.lower() in FORMAT_MAP and f.is_file()]
        logger.info("batch.ingest.started", count=len(files), study_id=study_id)

        results: list[IngestResult] = []
        for f in files:
            result = self.ingest(f, study_id)
            results.append(result)

        logger.info("batch.ingest.completed", count=len(results), study_id=study_id)
        return results
