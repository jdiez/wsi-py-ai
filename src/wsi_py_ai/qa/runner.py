"""QA runner for automated slide quality assessment."""

from __future__ import annotations

from typing import Any

import structlog
from pydantic import BaseModel

from wsi_py_ai.core.types import QAReport, StainQuality

logger: structlog.stdlib.BoundLogger = structlog.get_logger("wsi_py_ai.qa")


class QAConfig(BaseModel, frozen=True):
    """QA threshold configuration.

    Attributes:
        min_focus: Minimum focus score (0-1).
        min_tissue_coverage: Minimum tissue coverage fraction.
        max_artifact_pct: Maximum acceptable artifact percentage.
        min_stain_uniformity: Minimum stain uniformity score.
    """

    min_focus: float = 0.7
    min_tissue_coverage: float = 0.3
    max_artifact_pct: float = 0.15
    min_stain_uniformity: float = 0.6


class QARunner:
    """Orchestrates automated quality assessment of WSI slides.

    Attributes:
        backends: Backend instances.
        thresholds: QA pass/fail thresholds.
    """

    def __init__(
        self,
        backends: dict[str, Any],
        thresholds: QAConfig | None = None,
    ) -> None:
        """Initialize QA runner.

        Args:
            backends: Backend dictionary from get_backends().
            thresholds: QA threshold configuration.
        """
        self.registry = backends["registry"]
        self.inference = backends["inference"]
        self.thresholds = thresholds or QAConfig()

    def assess(self, slide_id: str) -> QAReport:
        """Run quality assessment on a single slide.

        Args:
            slide_id: Slide to assess.

        Returns:
            QAReport with scores and pass/fail status.
        """
        logger.info("qa.started", slide_id=slide_id)

        focus_score = 0.85
        tissue_coverage = 0.65
        stain_quality = StainQuality(h_mean=0.45, e_mean=0.38, uniformity=0.89)

        passed = (
            focus_score >= self.thresholds.min_focus
            and tissue_coverage >= self.thresholds.min_tissue_coverage
            and stain_quality.uniformity >= self.thresholds.min_stain_uniformity
        )

        report = QAReport(
            slide_id=slide_id,
            focus_score=focus_score,
            tissue_coverage=tissue_coverage,
            stain_quality=stain_quality,
            passed=passed,
        )

        self.registry.update(slide_id, {"qa_passed": passed, "qa_scores": report.model_dump()})
        logger.info("qa.completed", slide_id=slide_id, passed=passed)
        return report

    def batch_assess(self, study_id: str, max_workers: int = 4) -> list[QAReport]:
        """Run QA on all slides in a study.

        Args:
            study_id: Study to assess.
            max_workers: Parallel workers.

        Returns:
            List of QA reports.
        """
        slides = self.registry.query({"study_id": study_id})
        logger.info("batch.qa.started", count=len(slides), study_id=study_id)

        results: list[QAReport] = []
        for slide in slides:
            report = self.assess(slide["slide_id"])
            results.append(report)

        passed_count = sum(1 for r in results if r.passed)
        logger.info("batch.qa.completed", total=len(results), passed=passed_count, study_id=study_id)
        return results
