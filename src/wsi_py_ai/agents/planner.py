"""Planner agent — coordinates the multi-agent WSI pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agno.agent import Agent
from agno.models.anthropic import Claude

from wsi_py_ai.agents.base import AgentRole
from wsi_py_ai.tools.ingest_tools import ingest_batch, ingest_file
from wsi_py_ai.tools.qa_tools import qa_assess, qa_batch
from wsi_py_ai.tools.registry_tools import registry_query, registry_version_create

if TYPE_CHECKING:
    from wsi_py_ai.agents.config import AgentModelConfig

PLANNER_INSTRUCTIONS = [
    "You are the coordinator for a WSI (Whole Slide Image) processing pipeline.",
    "Decompose high-level goals into execution plans across specialist agents.",
    "Monitor progress and re-plan on failure.",
    "Decide execution order — parallelize independent steps when possible.",
    "Escalate to human when confidence is below threshold or policy decisions are needed.",
    "Never delete raw slides or skip de-identification.",
    "Track all decisions with reasoning for audit compliance.",
]


def create_planner_agent(model_config: AgentModelConfig | None = None) -> Agent:
    """Create the planner/coordinator agent.

    Args:
        model_config: Model configuration. Defaults to cloud config.

    Returns:
        Configured Agno Agent instance.
    """
    from wsi_py_ai.agents.config import AgentModelConfig

    config = model_config or AgentModelConfig()

    return Agent(
        model=Claude(id=config.planner),
        name=AgentRole.PLANNER.value,
        description="WSI Pipeline Coordinator — plans and orchestrates processing workflows",
        instructions=PLANNER_INSTRUCTIONS,
        tools=[ingest_file, ingest_batch, qa_assess, qa_batch, registry_query, registry_version_create],
    )


PlannerAgent = create_planner_agent
