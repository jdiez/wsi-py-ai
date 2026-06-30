# Pipeline Guide

This guide walks through a complete WSI processing workflow from raw slides to ML-ready datasets.

## End-to-End Flow

```
Raw Slides → Ingest → De-identify → QA → Registry → DataLoader → Training
```

## 1. Ingestion

Ingest slides from a scanner output directory:

```python
from wsi_py_ai.backends.factory import get_backends
from wsi_py_ai.config.settings import WSIPipelineConfig
from wsi_py_ai.ingest.ingester import WSIIngester

config = WSIPipelineConfig()
backends = get_backends(config)
ingester = WSIIngester(backends)

# Single file
result = ingester.ingest(
    source_path="/scanner/output/case001.svs",
    study_id="PROSTATE-2026",
)
print(f"Slide ID: {result.slide_id}")

# Batch ingest
results = ingester.batch_ingest(
    source_dir="/scanner/output/",
    study_id="PROSTATE-2026",
    pattern="*.svs",
    parallelism=8,
)
print(f"Ingested {len(results)} slides")
```

### CLI

```bash
wsi ingest file /scanner/output/case001.svs --study-id PROSTATE-2026
wsi ingest batch /scanner/output/ --study-id PROSTATE-2026 --pattern "*.svs"
```

## 2. De-identification

Remove all Protected Health Information (PHI):

```python
from wsi_py_ai.deid.deidentifier import DeidProfile, WSIDeidentifier

deidentifier = WSIDeidentifier(backends, profile=DeidProfile.DICOM_ANNEX_E)

# Single slide
result = deidentifier.deidentify(slide_id="abc-123")

# All slides in a study
results = deidentifier.batch_deidentify(study_id="PROSTATE-2026")
```

### CLI

```bash
wsi deid run --slide-id abc-123
wsi deid batch --study-id PROSTATE-2026
```

## 3. Quality Assessment

Run automated QA to detect quality issues:

```python
from wsi_py_ai.qa.runner import QAConfig, QARunner

# Custom thresholds
thresholds = QAConfig(min_focus=0.8, min_tissue_coverage=0.4)
runner = QARunner(backends, thresholds=thresholds)

report = runner.assess(slide_id="abc-123")
print(f"Passed: {report.passed}")
print(f"Focus: {report.focus_score}")
print(f"Tissue: {report.tissue_coverage}")

# Batch QA
reports = runner.batch_assess(study_id="PROSTATE-2026")
passed = [r for r in reports if r.passed]
print(f"{len(passed)}/{len(reports)} passed QA")
```

### CLI

```bash
wsi qa assess --slide-id abc-123
wsi qa batch --study-id PROSTATE-2026
```

## 4. Registry and Versioning

Query slides and create reproducible dataset versions:

```python
from wsi_py_ai.registry.registry import DatasetRegistry

registry = DatasetRegistry(backends)

# Query by attributes
slides = registry.query(study_id="PROSTATE-2026", qa_passed=True)

# Create a versioned dataset
version = registry.create_version(
    name="prostate-grading-v1",
    splits={"train": 0.7, "val": 0.15, "test": 0.15},
    stratify_by="grade",
)
print(f"Version: {version.name}, Slides: {len(version.slide_ids)}")
```

### CLI

```bash
wsi registry query --study-id PROSTATE-2026 --qa-passed
wsi registry version --name prostate-grading-v1
```

## 5. DataLoader

Configure optimized tile loading for training:

```python
from wsi_py_ai.dataloader.loader import (
    CacheConfig,
    TilingConfig,
    WSIDataLoader,
    pretile_dataset,
)

# Pre-tile for maximum speed
pretile_dataset(
    registry_version="prostate-grading-v1",
    output_format="webdataset",
    tiling=TilingConfig(tile_size=512, magnification=20.0, overlap=64),
    max_workers=16,
)

# Or stream tiles on-the-fly
loader = WSIDataLoader(
    registry_version="prostate-grading-v1",
    split="train",
    tiling=TilingConfig(tile_size=256, tissue_threshold=0.5),
    cache=CacheConfig(l2_max_gb=200, prefetch_batches=8),
    batch_size=64,
    num_workers=8,
    augmentations=("random_flip", "color_jitter", "stain_augment"),
)
```

### CLI

```bash
wsi dataloader pretile --version prostate-grading-v1 --tile-size 512
wsi dataloader stream --version prostate-grading-v1 --batch-size 64
```

## Complete Pipeline (CLI)

```bash
# One-shot: ingest → deid → qa for a study
wsi pipeline run --source-dir /scanner/output/ --study-id PROSTATE-2026
```
