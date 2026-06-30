# Multi-Agent System

`wsi-py-ai` includes a multi-agent orchestration layer built on the [Agno](https://github.com/agno-agi/agno) framework. Seven specialist agents collaborate to manage the WSI processing pipeline autonomously.

## Installation

```bash
pip install wsi-py-ai[agentic]
```

## Architecture

```
┌─────────────────────────────────────────────────┐
│              Planner Agent                       │
│   (Coordinator — decomposes goals into plans)   │
├────────┬────────┬────────┬──────────┬───────────┤
│ Ingest │  Deid  │   QA   │ Registry │ Training  │
│ Agent  │ Agent  │ Agent  │  Agent   │  Agent    │
├────────┴────────┴────────┴──────────┴───────────┤
│              Recovery Agent                      │
│   (Failure diagnosis and retry orchestration)   │
├─────────────────────────────────────────────────┤
│         Guardrails & Audit Trail                │
└─────────────────────────────────────────────────┘
```

## Agents

### Planner

The coordinator agent that decomposes high-level goals into execution plans across specialist agents. Decides execution order, parallelizes independent steps, and escalates to humans when confidence is low.

### Ingest Agent

Handles complex ingestion scenarios: format detection when extensions are wrong, corrupted file recovery, duplicate detection, and retry scheduling.

### Deid Agent

Ensures complete PHI removal. Verifies de-identification completeness, handles institution-specific metadata formats, and flags uncertain cases conservatively.

### QA Agent

Pathology QA specialist that goes beyond pass/fail. Diagnoses root causes of quality issues, detects systematic problems (scanner drift, staining inconsistency), and supports partial acceptance.

### Registry Agent

Manages dataset curation and metadata enrichment. Resolves conflicts, validates dataset cohesion for ML training, and creates reproducible versioned datasets.

### Training Agent

Optimizes data loading and tiling for ML workflows. Recommends tile sizes based on model architecture, handles class imbalance, and monitors throughput.

### Recovery Agent

Diagnoses pipeline failures and orchestrates recovery. Categorizes failures (transient/permanent/unknown), implements exponential backoff, and quarantines problematic slides.

## Model Configuration

### Cloud Models (Default)

```python
from wsi_py_ai.agents.config import AgentModelConfig

config = AgentModelConfig()
# planner:  claude-sonnet-4-6
# qa:       claude-sonnet-4-6
# deid:     claude-haiku-4-5
# ingest:   claude-haiku-4-5
# registry: claude-sonnet-4-6
# training: claude-sonnet-4-6
# recovery: claude-sonnet-4-6
```

### Local Models (On-Premise)

```python
from wsi_py_ai.agents.config import LocalAgentModelConfig

config = LocalAgentModelConfig()
# planner:  llama3.1:70b-instruct
# qa:       llama3.2-vision:90b
# deid:     llama3.1:8b-instruct
# ingest:   llama3.1:8b-instruct
# registry: llama3.1:70b-instruct
# training: llama3.1:70b-instruct
# recovery: llama3.1:8b-instruct
# inference_server: ollama
# inference_url: http://localhost:11434
```

## Guardrails

Safety constraints that agents cannot override:

| Guardrail | Default | Description |
|-----------|---------|-------------|
| `never_delete_raw_slides` | `True` | Raw files are immutable |
| `never_skip_deid` | `True` | De-identification is mandatory |
| `min_confidence_threshold` | `0.85` | Below this, escalate to human |
| `max_retries_before_escalate` | `3` | Retry limit before human review |
| `require_human_for_deid_failure` | `True` | Deid failures always need human |
| `max_concurrent_agents` | `5` | Concurrency cap |
| `audit_all_decisions` | `True` | Log every decision |

```python
from wsi_py_ai.orchestration.guardrails import AgentGuardrails

guardrails = AgentGuardrails(min_confidence_threshold=0.9)
guardrails.allows_autonomous_action(confidence=0.87)  # False
guardrails.should_escalate(retries=4)  # True
```

## Decision Audit Log

All agent decisions are recorded in an append-only JSONL log for regulatory compliance:

```python
from pathlib import Path
from wsi_py_ai.memory.audit import DecisionAuditLog
from wsi_py_ai.agents.base import AgentDecision, AgentRole

log = DecisionAuditLog(log_dir=Path("./audit"))

decision = AgentDecision(
    agent=AgentRole.QA,
    decision="Flag slide for re-scan",
    reasoning="Focus score 0.45 below threshold 0.7, affecting >60% of tissue area",
    confidence=0.92,
    alternatives_considered=("partial_accept", "manual_review"),
)

log.record(agent_role=AgentRole.QA, decision=decision)
entries = log.query(agent_role=AgentRole.QA)
```

## CLI Usage

```bash
# Show agent configuration and guardrails
wsi agent status

# Run the planner with a natural language goal
wsi agent run "Ingest all SVS files from /data/incoming, run QA, and create a dataset version"

# Use local models
wsi agent run "Assess quality of study STUDY-001" --model-config local
```

## Tools

Each agent has access to pipeline operations as Agno tools:

| Tool | Module | Description |
|------|--------|-------------|
| `ingest_file` | `tools.ingest_tools` | Ingest single WSI file |
| `ingest_batch` | `tools.ingest_tools` | Batch ingest from directory |
| `deid_run` | `tools.deid_tools` | De-identify single slide |
| `deid_batch` | `tools.deid_tools` | Batch de-identification |
| `qa_assess` | `tools.qa_tools` | QA single slide |
| `qa_batch` | `tools.qa_tools` | Batch QA assessment |
| `registry_query` | `tools.registry_tools` | Query slide catalog |
| `registry_register` | `tools.registry_tools` | Register a slide |
| `registry_version_create` | `tools.registry_tools` | Create dataset version |
| `dataloader_pretile` | `tools.dataloader_tools` | Pre-tile for training |
| `dataloader_stream` | `tools.dataloader_tools` | Configure streaming loader |
