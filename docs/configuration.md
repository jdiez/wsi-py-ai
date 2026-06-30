# Configuration

`wsi-py-ai` uses [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) for configuration. All values can be set via environment variables with the `WSI_` prefix.

## Pipeline Configuration

::: wsi_py_ai.config.settings.WSIPipelineConfig
    options:
      show_root_heading: true
      members_order: source

## Backend Modes

### Local Mode

Local mode uses the filesystem, SQLite, and multiprocessing. No external services required.

```bash
export WSI_MODE=local
export WSI_LOCAL_BASE_DIR=/data/wsi-pipeline
export WSI_LOCAL_DB=/data/wsi-pipeline/registry.db
export WSI_LOCAL_MODELS_DIR=/data/models
export WSI_LOCAL_DEVICE=cuda:0
```

### GCP Mode

GCP mode uses Google Cloud Storage, BigQuery, Dataflow, and Vertex AI.

```bash
export WSI_MODE=gcp
export WSI_GCP_PROJECT=my-project
export WSI_GCP_REGION=us-central1
export WSI_RAW_BUCKET=my-raw-slides
export WSI_CLEAN_BUCKET=my-clean-slides
export WSI_REGISTRY_DATASET=wsi_registry
export WSI_QA_ENDPOINT=projects/my-project/locations/us-central1/endpoints/12345
```

## PostgreSQL Registry

Use PostgreSQL instead of SQLite for multi-user production deployments:

```bash
export WSI_REGISTRY_BACKEND=postgres
export WSI_POSTGRES_URL=postgresql://user:pass@host:5432/wsi_db
```

Requires: `pip install wsi-py-ai[postgres]`

## QA Thresholds

Quality assessment thresholds are configurable:

```bash
export WSI_QA_MIN_FOCUS=0.7
export WSI_QA_MIN_TISSUE_COVERAGE=0.3
export WSI_QA_MAX_ARTIFACT_PCT=0.15
export WSI_QA_MIN_STAIN_UNIFORMITY=0.6
```

## Configuration File

Alternatively, use a `.env` file in the working directory:

```ini
WSI_MODE=local
WSI_LOCAL_BASE_DIR=/data/wsi-pipeline
WSI_LOCAL_DB=/data/wsi-pipeline/registry.db
WSI_QA_MIN_FOCUS=0.8
```

## Viewing Current Configuration

```bash
wsi config show
```
