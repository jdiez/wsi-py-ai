# SPECS — wsi-py-ai

> Development contract and single source of truth for project identity, architecture, and constraints.
> Auto-generated from cookie-claude template. Update with: `/update-specs`

## Identity

| Field | Value |
|-------|-------|
| **Name** | wsi-py-ai |
| **Package** | `wsi_py_ai` |
| **Description** | WSI Processing Pipeline — ingestion, de-identification, registry, DataLoader optimization, and automated QA for whole slide images. Dual-mode: local on-premise and GCP cloud. |
| **Author** | Javier Díez Pérez <javier@example.com> |
| **License** | Apache Software License 2.0 |
| **Python** | >=3.10, <4.0 |

## Tech Stack

| Layer | Choice | Notes |
|-------|--------|-------|
| Package manager | uv | Sole environment/dependency tool |
| Build backend | hatchling | src layout |
| Validation | pydantic v2 | Frozen models, mypy plugin |
| Logging | structlog | Structured events, stdlib integration |
| Linting | ruff | Line-length 120, Google docstrings |
| Type checking | mypy | Strict mode |
| Testing | pytest | Doctests enabled, no `__init__.py` in tests/ |
| Security | bandit | Pre-commit + CI |
| Dep auditing | deptry | Detect unused/missing deps |
| Documentation | MkDocs | Material theme + mkdocstrings |
| Multi-version | tox-uv | Python 3.10–3.14 |
| CI/CD | GitHub Actions | PR checks + release workflow |
| Coverage | Codecov | Integrated with CI |

## Architecture

### Layout

```
src/wsi_py_ai/
├── __init__.py          # Package root, version export
└── (modules)            # Domain modules added here
```

### Module Boundaries

<!-- Define module responsibilities as the project grows -->
| Module | Responsibility | Public API |
|--------|---------------|------------|
| `wsi_py_ai` | Package root | TBD |

### Data Flow

<!-- Describe how data moves through the system -->
```
Input → Validation (pydantic) → Processing → Output
```

## API Surface

<!-- Define the public API contract -->
| Symbol | Type | Stable | Notes |
|--------|------|--------|-------|
| TBD | — | — | Define as modules are added |

## Testing Strategy

| Layer | Tool | Location | Coverage Target |
|-------|------|----------|----------------|
| Unit | pytest | `tests/test_*.py` | Core logic |
| Type | mypy (strict) | All source | 100% annotated |
| Lint | ruff + bandit | All source | Zero violations |
| Integration | pytest | `tests/` | External boundaries |
| Coverage | Codecov | CI | Track regressions |

## Deployment
| Target | Method | Trigger |
|--------|--------|---------|
| Container | Dockerfile (multi-stage) | Manual / CI |

## Constraints

- **uv only** — no pip, poetry, conda
- **Immutable models** — pydantic `frozen=True`, `tuple` over `list` for collections
- **Strict typing** — mypy strict, no untyped `# type: ignore`
- **Security gate** — bandit must pass before merge
- **Google docstrings** — all public symbols documented
- **No test `__init__.py`** — pytest discovers without it
- **src layout** — import path is `from wsi_py_ai import ...`

## Decision Log

<!-- Record architecture decisions as they're made -->
| Date | Decision | Rationale |
|------|----------|-----------|
| (project creation) | src layout | Template default |
| (project creation) | pydantic + structlog | Validation + observability from day one |
| (project creation) | MkDocs for docs | Auto-generated API docs from docstrings |
