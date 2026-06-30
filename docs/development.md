# Development

## Setup

```bash
git clone https://github.com/jdiez/wsi-py-ai.git
cd wsi-py-ai
uv sync
uv run pre-commit install
```

## Commands

```bash
make install     # uv sync + pre-commit install
make check       # Lock, pre-commit, mypy, deptry
make security    # Bandit security scan
make test        # pytest with coverage
make docs        # Serve docs locally (localhost:8000)
make docs-test   # Verify docs build
make build       # Build wheel
```

## Testing

```bash
# Run all tests
uv run python -m pytest

# With coverage
uv run python -m pytest --cov=src

# Single test file
uv run python -m pytest tests/test_types.py -v
```

## Type Checking

```bash
uv run mypy  # Strict mode, 51 source files
```

## Linting

```bash
uv run ruff check src/     # Lint
uv run ruff format src/    # Format
```

## Security

```bash
uv run bandit -r src/ -c pyproject.toml -ll
```

## Adding Dependencies

```bash
uv add pydantic              # Runtime
uv add --dev pytest          # Dev (PEP 735)
uv add --group docs mkdocs   # Named group
```

## Project Structure

```
src/wsi_py_ai/
├── __init__.py              # Package root, version
├── config/
│   └── settings.py          # Pydantic settings (WSI_ env prefix)
├── core/
│   ├── types.py             # Shared pydantic models (frozen)
│   └── slide.py             # SlideReader ABC + LocalSlideReader
├── backends/
│   ├── base.py              # ABC interfaces (Storage, Registry, Compute, Inference)
│   ├── local.py             # Local implementations (filesystem, SQLite, multiprocessing)
│   ├── gcp.py               # GCP stubs (GCS, BigQuery, Dataflow, Vertex)
│   └── factory.py           # get_backends(config) dispatcher
├── ingest/
│   └── ingester.py          # WSIIngester (single + batch)
├── deid/
│   └── deidentifier.py      # WSIDeidentifier (profiles, batch)
├── registry/
│   └── registry.py          # DatasetRegistry + DatasetVersion
├── dataloader/
│   └── loader.py            # WSIDataLoader + pretile_dataset
├── qa/
│   └── runner.py            # QARunner (scoring, thresholds)
├── agents/
│   ├── __init__.py          # Lazy imports (agno optional)
│   ├── base.py              # AgentRole, AgentMessage, AgentDecision
│   ├── config.py            # AgentModelConfig, LocalAgentModelConfig
│   ├── planner.py           # Coordinator agent
│   ├── ingest_agent.py      # Ingestion specialist
│   ├── deid_agent.py        # De-identification specialist
│   ├── qa_agent.py          # QA specialist
│   ├── registry_agent.py    # Registry/curation specialist
│   ├── training_agent.py    # DataLoader/training specialist
│   └── recovery_agent.py    # Failure recovery specialist
├── tools/
│   ├── __init__.py          # Lazy imports (agno optional)
│   ├── ingest_tools.py      # @tool wrappers for ingestion
│   ├── deid_tools.py        # @tool wrappers for deid
│   ├── qa_tools.py          # @tool wrappers for QA
│   ├── registry_tools.py    # @tool wrappers for registry
│   └── dataloader_tools.py  # @tool wrappers for dataloader
├── memory/
│   ├── __init__.py
│   └── audit.py             # DecisionAuditLog (JSONL compliance)
├── orchestration/
│   ├── __init__.py
│   └── guardrails.py        # AgentGuardrails safety model
└── cli/
    ├── __init__.py           # Typer app with 8 subcommands
    ├── ingest_cmd.py
    ├── deid_cmd.py
    ├── registry_cmd.py
    ├── dataloader_cmd.py
    ├── qa_cmd.py
    ├── pipeline_cmd.py
    ├── config_cmd.py
    └── agent_cmd.py
```

## Optional Dependency Groups

| Group | Packages | Use Case |
|-------|----------|----------|
| `gcp` | google-cloud-storage, bigquery, aiplatform, pubsub | GCP backend |
| `ml` | torch, torchvision, Pillow, scikit-image | Training/inference |
| `agentic` | agno | Multi-agent system |
| `orchestration-prefect` | prefect | Workflow orchestration |
| `postgres` | psycopg2-binary, sqlalchemy | PostgreSQL registry |
| `all` | All of the above | Full installation |
