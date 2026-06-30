# wsi-py-ai

[![Release](https://img.shields.io/github/v/release/jdiez/wsi-py-ai)](https://img.shields.io/github/v/release/jdiez/wsi-py-ai)
[![Build status](https://img.shields.io/github/actions/workflow/status/jdiez/wsi-py-ai/main.yml?branch=main)](https://github.com/jdiez/wsi-py-ai/actions/workflows/main.yml?query=branch%3Amain)
[![License](https://img.shields.io/github/license/jdiez/wsi-py-ai)](https://img.shields.io/github/license/jdiez/wsi-py-ai)

**WSI Processing Pipeline** — ingestion, de-identification, registry, DataLoader optimization, and automated QA for whole slide images. Dual-mode: local on-premise and GCP cloud.

## Features

- **Multi-format ingestion** — SVS, NDPI, DICOM, iSyntax, MRXS, TIFF, BIF
- **HIPAA-compliant de-identification** — metadata stripping, label redaction, DICOM Annex E profiles
- **Dataset registry** — versioned slide catalogs with train/val/test splitting
- **Optimized DataLoader** — tiling, caching, prefetching for PyTorch training
- **Automated QA** — focus detection, tissue coverage, stain uniformity scoring
- **Dual-mode backends** — same API on local hardware or GCP (GCS, BigQuery, Dataflow, Vertex AI)
- **Multi-agent orchestration** — 7 specialist AI agents via Agno framework for autonomous pipeline management

## Quick Start

### Installation

```bash
# Core package (local mode)
pip install wsi-py-ai

# With GCP backends
pip install wsi-py-ai[gcp]

# With ML/training support
pip install wsi-py-ai[ml]

# With multi-agent system
pip install wsi-py-ai[agentic]

# Everything
pip install wsi-py-ai[all]
```

### Development Setup

```bash
git clone https://github.com/jdiez/wsi-py-ai.git
cd wsi-py-ai
uv sync
uv run wsi --help
```

### Basic Usage

```bash
# Ingest slides
wsi ingest file /path/to/slide.svs --study-id STUDY-001

# De-identify
wsi deid run --slide-id <id>

# Run QA
wsi qa assess --slide-id <id>

# Query registry
wsi registry query --study-id STUDY-001

# Show configuration
wsi config show

# Agent system status
wsi agent status
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLI (typer)                           │
├─────────────────────────────────────────────────────────┤
│  ingest │ deid │ registry │ dataloader │ qa │ agent     │
├─────────────────────────────────────────────────────────┤
│              Backend Abstraction Layer                   │
│   StorageBackend │ RegistryBackend │ ComputeBackend     │
├──────────────────┼──────────────────┼───────────────────┤
│  Local Mode      │                  │  GCP Mode         │
│  - Filesystem    │                  │  - GCS            │
│  - SQLite        │                  │  - BigQuery       │
│  - Multiprocess  │                  │  - Dataflow       │
│  - (stub)        │                  │  - Vertex AI      │
└──────────────────┴──────────────────┴───────────────────┘
```

## Configuration

All settings are environment-driven with the `WSI_` prefix:

| Variable | Default | Description |
|----------|---------|-------------|
| `WSI_MODE` | `local` | Backend mode: `local` or `gcp` |
| `WSI_LOCAL_BASE_DIR` | `/data/wsi-pipeline` | Local storage root |
| `WSI_LOCAL_DB` | `wsi-registry.db` | SQLite database path |
| `WSI_GCP_PROJECT` | — | GCP project ID |
| `WSI_RAW_BUCKET` | — | GCS bucket for raw slides |

See [Configuration](configuration.md) for the full reference.

## License

MIT
