"""Agno tools wrapping the WSI quality assessment module."""

from __future__ import annotations

import json

from agno.tools.decorator import tool

from wsi_py_ai.backends.factory import get_backends
from wsi_py_ai.config.settings import WSIPipelineConfig
from wsi_py_ai.qa.runner import QARunner


@tool
def qa_assess(slide_id: str) -> str:
    """Assess quality of a single WSI slide.

    Args:
        slide_id: Identifier of the slide to assess.

    Returns:
        JSON string with QA report (dimensions, scores, pass/fail, issues).
    """
    config = WSIPipelineConfig()
    backends = get_backends(config)
    runner = QARunner(backends)
    report = runner.assess(slide_id=slide_id)
    return json.dumps(report.model_dump(), default=str)


@tool
def qa_batch(study_id: str) -> str:
    """Assess quality of all slides in a study.

    Args:
        study_id: Study identifier — all slides in this study will be assessed.

    Returns:
        JSON string with list of QA reports.
    """
    config = WSIPipelineConfig()
    backends = get_backends(config)
    runner = QARunner(backends)
    reports = runner.batch_assess(study_id=study_id)
    return json.dumps([r.model_dump() for r in reports], default=str)
