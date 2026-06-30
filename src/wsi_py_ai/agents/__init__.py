"""Multi-agentic WSI processing system built on Agno.

Agent classes require the 'agentic' optional dependency group:
    uv pip install wsi-py-ai[agentic]
"""

from wsi_py_ai.agents.base import AgentDecision, AgentMessage, AgentRole, Priority

__all__ = [
    "AgentDecision",
    "AgentMessage",
    "AgentRole",
    "DeidAgent",
    "IngestAgent",
    "PlannerAgent",
    "Priority",
    "QAAgent",
    "RecoveryAgent",
    "RegistryAgent",
    "TrainingAgent",
]


def __getattr__(name: str) -> object:
    """Lazy-load agent classes that depend on agno."""
    _agent_map = {
        "DeidAgent": "wsi_py_ai.agents.deid_agent",
        "IngestAgent": "wsi_py_ai.agents.ingest_agent",
        "PlannerAgent": "wsi_py_ai.agents.planner",
        "QAAgent": "wsi_py_ai.agents.qa_agent",
        "RecoveryAgent": "wsi_py_ai.agents.recovery_agent",
        "RegistryAgent": "wsi_py_ai.agents.registry_agent",
        "TrainingAgent": "wsi_py_ai.agents.training_agent",
    }
    if name in _agent_map:
        import importlib

        module = importlib.import_module(_agent_map[name])
        return getattr(module, name)
    msg = f"module 'wsi_py_ai.agents' has no attribute {name!r}"
    raise AttributeError(msg)
