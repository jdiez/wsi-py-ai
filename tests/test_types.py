"""Tests for core type definitions."""

from wsi_py_ai.core.types import (
    ArtifactRegion,
    DeidResult,
    IngestResult,
    QAReport,
    SlideFormat,
    SlideMetadata,
    StainQuality,
    StainType,
)


def test_slide_metadata_immutable():
    meta = SlideMetadata(
        slide_id="SLIDE-001",
        study_id="STUDY-1",
        format=SlideFormat.SVS,
        magnification=40.0,
    )
    assert meta.slide_id == "SLIDE-001"
    assert meta.format == SlideFormat.SVS


def test_qa_report_pass():
    report = QAReport(
        slide_id="SLIDE-001",
        focus_score=0.9,
        tissue_coverage=0.7,
        stain_quality=StainQuality(h_mean=0.5, e_mean=0.4, uniformity=0.9),
        passed=True,
    )
    assert report.passed is True
    assert report.focus_score == 0.9


def test_qa_report_with_artifacts():
    artifact = ArtifactRegion(artifact_type="fold", area_pct=0.03, bbox=(100, 100, 200, 200))
    report = QAReport(
        slide_id="SLIDE-002",
        focus_score=0.5,
        tissue_coverage=0.6,
        artifact_regions=(artifact,),
        passed=False,
    )
    assert len(report.artifact_regions) == 1
    assert report.artifact_regions[0].artifact_type == "fold"


def test_ingest_result():
    meta = SlideMetadata(slide_id="S1", study_id="ST1", format=SlideFormat.NDPI)
    result = IngestResult(slide_id="S1", storage_uri="/data/raw/S1.ndpi", metadata=meta)
    assert result.storage_uri == "/data/raw/S1.ndpi"


def test_deid_result():
    result = DeidResult(slide_id="S1", clean_uri="/data/clean/S1.svs")
    assert result.metadata_stripped is True
    assert result.labels_redacted is True


def test_stain_types():
    assert StainType.HE.value == "H&E"
    assert StainType.IHC_PDL1.value == "IHC-PD-L1"


def test_slide_format_values():
    assert SlideFormat.SVS.value == "svs"
    assert SlideFormat.DICOM.value == "dcm"
