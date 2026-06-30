"""Shared type definitions for the WSI pipeline."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class SlideFormat(str, Enum):
    """Supported WSI file formats."""

    SVS = "svs"
    NDPI = "ndpi"
    DICOM = "dcm"
    ISYNTAX = "isyntax"
    MRXS = "mrxs"
    TIFF = "tiff"
    BIF = "bif"


class StainType(str, Enum):
    """Common stain types."""

    HE = "H&E"
    IHC_PDL1 = "IHC-PD-L1"
    IHC_KI67 = "IHC-Ki67"
    IHC_HER2 = "IHC-HER2"
    IHC_ER = "IHC-ER"
    IHC_PR = "IHC-PR"
    OTHER = "other"


class QADimension(str, Enum):
    """Quality assurance dimensions."""

    FOCUS = "focus"
    COVERAGE = "coverage"
    ARTIFACTS = "artifacts"
    STAIN = "stain"
    SCANNER = "scanner"
    COMPRESSION = "compression"
    MAGNIFICATION = "magnification"
    COMPLETENESS = "completeness"


class SlideMetadata(BaseModel, frozen=True):
    """Metadata extracted from a WSI file."""

    slide_id: str
    study_id: str
    format: SlideFormat
    scanner: str = ""
    magnification: float = 40.0
    width_px: int = 0
    height_px: int = 0
    stain: StainType = StainType.HE
    tissue_type: str = ""
    file_size_bytes: int = 0


class ArtifactRegion(BaseModel, frozen=True):
    """A detected artifact region in a slide."""

    artifact_type: str
    area_pct: float
    bbox: tuple[int, int, int, int]


class StainQuality(BaseModel, frozen=True):
    """Stain quality metrics."""

    h_mean: float
    e_mean: float
    uniformity: float


class QAReport(BaseModel, frozen=True):
    """Quality assessment report for a single slide."""

    slide_id: str
    focus_score: float
    tissue_coverage: float
    artifact_regions: tuple[ArtifactRegion, ...] = ()
    stain_quality: StainQuality | None = None
    passed: bool = False


class IngestResult(BaseModel, frozen=True):
    """Result of ingesting a single slide."""

    slide_id: str
    storage_uri: str
    metadata: SlideMetadata


class DeidResult(BaseModel, frozen=True):
    """Result of de-identifying a single slide."""

    slide_id: str
    clean_uri: str
    metadata_stripped: bool = True
    labels_redacted: bool = True
    annotations_stripped: bool = True
