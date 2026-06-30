# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-30

### Added

- **GCP backends** (fully implemented):
  - GCSStorageBackend: upload, download, list_files, exists via google-cloud-storage
  - BigQueryRegistryBackend: register, query (parameterized), update via google-cloud-bigquery
  - DataflowComputeBackend: batch processing via Apache Beam pipeline
  - VertexInferenceBackend: batch prediction via Vertex AI endpoints
- **Local inference** (torch): TorchScript model loading + GPU/CPU forward pass
- **OpenSlideReader**: full WSI access via openslide-python (read_region, get_properties, get_thumbnail, get_metadata)
- **Prefect orchestration**: `@flow`/`@task` pipeline with retries (ingest 3x, deid 2x, QA 2x)
- **PostgreSQL registry**: SQLAlchemy-based backend with JSONB queries and upsert semantics
- **CLI `wsi pipeline prefect`**: trigger Prefect-managed pipeline from CLI
- **Config**: `registry_backend` and `postgres_url` settings for backend selection
- **Factory**: automatic dispatch to PostgresRegistryBackend when configured
- **`openslide-python`** added to `ml` optional group

### Changed

- GCP backends no longer raise NotImplementedError — they use real SDK calls
- LocalInferenceBackend loads TorchScript models instead of raising NotImplementedError
- LocalSlideReader preserved as fallback; OpenSlideReader is the production reader

## [0.1.0] - 2026-06-30

### Added

- **Core pipeline modules**: ingestion, de-identification, registry, dataloader, QA
- **Backend abstraction layer**: StorageBackend, RegistryBackend, ComputeBackend, InferenceBackend ABCs
- **Local backends**: filesystem storage, SQLite registry, ProcessPoolExecutor compute
- **GCP backend stubs**: GCS, BigQuery, Dataflow, Vertex AI (ready for implementation)
- **SlideReader**: ABC with LocalSlideReader for OpenSlide-based slide access
- **Pydantic models**: SlideMetadata, QAReport, IngestResult, DeidResult (all frozen/immutable)
- **Configuration**: pydantic-settings with `WSI_` env prefix, dual-mode (local/gcp)
- **CLI**: 8 Typer subcommands (ingest, deid, registry, dataloader, qa, pipeline, config, agent)
- **Multi-agent system** (Agno framework):
  - 7 specialist agents: Planner, Ingest, Deid, QA, Registry, Training, Recovery
  - Agno @tool wrappers for all pipeline operations
  - AgentModelConfig for cloud (Claude) and local (Ollama/vLLM) model selection
  - AgentGuardrails safety model (never delete raw, never skip deid, confidence thresholds)
  - DecisionAuditLog for regulatory compliance (append-only JSONL)
  - Lazy imports for optional `agno` dependency
- **Quality tooling**: ruff, mypy strict, bandit, deptry, pre-commit, pytest
- **Documentation**: MkDocs Material with full API reference, pipeline guide, agent docs
- **CI**: GitHub Actions workflows for PR checks and releases

[0.2.0]: https://github.com/jdiez/wsi-py-ai/releases/tag/v0.2.0
[0.1.0]: https://github.com/jdiez/wsi-py-ai/releases/tag/v0.1.0
