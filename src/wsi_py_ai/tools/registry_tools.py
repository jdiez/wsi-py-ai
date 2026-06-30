"""Agno tools wrapping the WSI dataset registry module."""

from __future__ import annotations

import json

from agno.tools.decorator import tool

from wsi_py_ai.backends.factory import get_backends
from wsi_py_ai.config.settings import WSIPipelineConfig
from wsi_py_ai.registry.registry import DatasetRegistry


@tool
def registry_query(filters: str) -> str:
    """Query the slide registry with filters.

    Args:
        filters: JSON string of key-value filter criteria (e.g. '{"study_id": "STUDY-001"}').

    Returns:
        JSON string with list of matching slide records.
    """
    config = WSIPipelineConfig()
    backends = get_backends(config)
    registry = DatasetRegistry(backends)
    filter_dict = json.loads(filters)
    results = registry.query(**filter_dict)
    return json.dumps(results, default=str)


@tool
def registry_register(slide_id: str, metadata: str) -> str:
    """Register a slide in the dataset registry.

    Args:
        slide_id: Unique identifier for the slide.
        metadata: JSON string of slide metadata.

    Returns:
        JSON confirmation of registration.
    """
    config = WSIPipelineConfig()
    backends = get_backends(config)
    registry = DatasetRegistry(backends)
    meta_dict = json.loads(metadata)
    registry.register(slide_id=slide_id, metadata=meta_dict)
    return json.dumps({"status": "registered", "slide_id": slide_id})


@tool
def registry_version_create(name: str, query: str = "") -> str:
    """Create a versioned dataset snapshot.

    Args:
        name: Name for the dataset version.
        query: Filter expression for which slides to include.

    Returns:
        JSON string with version details (name, slide_ids, splits).
    """
    config = WSIPipelineConfig()
    backends = get_backends(config)
    registry = DatasetRegistry(backends)
    version = registry.create_version(name=name, query=query)
    return json.dumps({
        "name": version.name,
        "query": version.query,
        "splits": version.splits,
        "slide_count": len(version.slide_ids),
    })
