# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.1.0]: https://github.com/jdiez/wsi-py-ai/releases/tag/v0.1.0
