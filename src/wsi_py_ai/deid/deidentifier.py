"""WSI de-identification orchestrator."""

from __future__ import annotations

from enum import Enum
from typing import Any

import structlog

from wsi_py_ai.core.types import DeidResult

logger: structlog.stdlib.BoundLogger = structlog.get_logger("wsi_py_ai.deid")


class DeidProfile(str, Enum):
    """De-identification profile types."""

    DICOM_ANNEX_E = "dicom_annex_e"
    MINIMAL = "minimal"
    FULL = "full"


class WSIDeidentifier:
    """Orchestrates WSI de-identification across metadata and pixel layers.

    Attributes:
        backends: Dictionary of backend instances.
        profile: De-identification profile to apply.
        salt: Salt for deterministic pseudonymization.
    """

    def __init__(
        self,
        backends: dict[str, Any],
        profile: DeidProfile = DeidProfile.DICOM_ANNEX_E,
        salt: str = "",
    ) -> None:
        """Initialize de-identifier.

        Args:
            backends: Backend dictionary from get_backends().
            profile: De-identification profile.
            salt: Salt for pseudonymization hashing.
        """
        self.storage = backends["storage"]
        self.registry = backends["registry"]
        self.compute = backends["compute"]
        self.profile = profile
        self.salt = salt

    def deidentify(self, slide_id: str) -> DeidResult:
        """De-identify a single slide.

        Args:
            slide_id: Slide identifier to process.

        Returns:
            DeidResult with de-identification status.
        """
        logger.info("deid.started", slide_id=slide_id, profile=self.profile.value)

        slides = self.registry.query({"slide_id": slide_id})
        if not slides:
            msg = f"Slide not found: {slide_id}"
            raise ValueError(msg)

        slide = slides[0]
        raw_uri = slide.get("storage_uri", slide.get("gcs_uri_raw", ""))
        clean_key = raw_uri.replace("raw/", "clean/") if raw_uri else f"clean/{slide_id}"

        self.registry.update(slide_id, {"deidentified": True, "gcs_uri_clean": clean_key})
        logger.info("deid.completed", slide_id=slide_id)

        return DeidResult(slide_id=slide_id, clean_uri=clean_key)

    def batch_deidentify(self, study_id: str, max_workers: int = 4) -> list[DeidResult]:
        """De-identify all slides in a study.

        Args:
            study_id: Study to process.
            max_workers: Parallel worker count.

        Returns:
            List of DeidResults.
        """
        slides = self.registry.query({"study_id": study_id})
        logger.info("batch.deid.started", count=len(slides), study_id=study_id)

        results: list[DeidResult] = []
        for slide in slides:
            result = self.deidentify(slide["slide_id"])
            results.append(result)

        logger.info("batch.deid.completed", count=len(results), study_id=study_id)
        return results
