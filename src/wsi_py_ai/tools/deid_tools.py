"""Agno tools wrapping the WSI de-identification module."""

from __future__ import annotations

import json

from agno.tools.decorator import tool

from wsi_py_ai.backends.factory import get_backends
from wsi_py_ai.config.settings import WSIPipelineConfig
from wsi_py_ai.deid.deidentifier import WSIDeidentifier


@tool
def deid_run(slide_id: str) -> str:
    """De-identify a single WSI slide, removing all PHI.

    Args:
        slide_id: Identifier of the slide to de-identify.

    Returns:
        JSON string with de-identification result (status, fields removed).
    """
    config = WSIPipelineConfig()
    backends = get_backends(config)
    deidentifier = WSIDeidentifier(backends)
    result = deidentifier.deidentify(slide_id=slide_id)
    return json.dumps(result.model_dump(), default=str)


@tool
def deid_batch(study_id: str) -> str:
    """De-identify all slides in a study.

    Args:
        study_id: Study identifier — all slides in this study will be de-identified.

    Returns:
        JSON string with list of de-identification results.
    """
    config = WSIPipelineConfig()
    backends = get_backends(config)
    deidentifier = WSIDeidentifier(backends)
    results = deidentifier.batch_deidentify(study_id=study_id)
    return json.dumps([r.model_dump() for r in results], default=str)
