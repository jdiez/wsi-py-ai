"""Dataset registry for slide catalog and version management."""

from __future__ import annotations

from typing import Any

import structlog

from wsi_py_ai.core.types import SlideMetadata

logger: structlog.stdlib.BoundLogger = structlog.get_logger("wsi_py_ai.registry")


class DatasetVersion:
    """A versioned dataset snapshot.

    Attributes:
        name: Version name (e.g., prostate-grading-v2).
        query: Query that defines the version contents.
        splits: Train/val/test split ratios.
        slide_ids: Slide IDs in this version.
    """

    def __init__(
        self,
        name: str,
        query: str,
        splits: dict[str, float] | None = None,
        slide_ids: tuple[str, ...] = (),
    ) -> None:
        """Initialize dataset version.

        Args:
            name: Human-readable version name.
            query: Filter query that defines membership.
            splits: Optional split ratios (e.g., {"train": 0.7}).
            slide_ids: Slide IDs belonging to this version.
        """
        self.name = name
        self.query = query
        self.splits = splits or {"train": 0.7, "val": 0.15, "test": 0.15}
        self.slide_ids = slide_ids


class DatasetRegistry:
    """Manages the slide catalog and dataset versioning.

    Attributes:
        backends: Dictionary of backend instances.
    """

    def __init__(self, backends: dict[str, Any]) -> None:
        """Initialize registry with backends.

        Args:
            backends: Backend dictionary from get_backends().
        """
        self.registry_backend = backends["registry"]

    def register(self, slide_id: str, metadata: SlideMetadata | dict[str, Any]) -> None:
        """Register a slide in the catalog.

        Args:
            slide_id: Unique slide identifier.
            metadata: Slide metadata (pydantic model or dict).
        """
        meta_dict = metadata.model_dump() if isinstance(metadata, SlideMetadata) else metadata
        self.registry_backend.register_slide(slide_id, meta_dict)
        logger.info("slide.registered", slide_id=slide_id)

    def query(
        self,
        tissue_type: str | None = None,
        stain: str | None = None,
        qa_passed: bool | None = None,
        study_id: str | None = None,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Query slides by attributes.

        Args:
            tissue_type: Filter by tissue type.
            stain: Filter by stain type.
            qa_passed: Filter by QA status.
            study_id: Filter by study.
            **kwargs: Additional filter key-value pairs.

        Returns:
            List of matching slide metadata dictionaries.
        """
        filters: dict[str, Any] = {**kwargs}
        if tissue_type is not None:
            filters["tissue_type"] = tissue_type
        if stain is not None:
            filters["stain"] = stain
        if qa_passed is not None:
            filters["qa_passed"] = qa_passed
        if study_id is not None:
            filters["study_id"] = study_id

        results: list[dict[str, Any]] = self.registry_backend.query(filters)
        return results

    def create_version(
        self,
        name: str,
        query: str = "",
        splits: dict[str, float] | None = None,
        stratify_by: str | None = None,
    ) -> DatasetVersion:
        """Create a versioned dataset from a query.

        Args:
            name: Version name.
            query: Filter expression (simplified for local mode).
            splits: Split ratios.
            stratify_by: Field to stratify splits by.

        Returns:
            DatasetVersion object.
        """
        all_slides = self.registry_backend.query({})
        slide_ids = tuple(s["slide_id"] for s in all_slides)

        version = DatasetVersion(name=name, query=query, splits=splits, slide_ids=slide_ids)
        logger.info("version.created", name=name, count=len(slide_ids), stratify_by=stratify_by)
        return version
