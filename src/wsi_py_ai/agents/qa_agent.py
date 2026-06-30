"""QA agent — diagnoses quality issues and recommends actions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agno.agent import Agent
from agno.models.anthropic import Claude

from wsi_py_ai.agents.base import AgentRole
from wsi_py_ai.tools.qa_tools import qa_assess, qa_batch

if TYPE_CHECKING:
    from wsi_py_ai.agents.config import AgentModelConfig

QA_INSTRUCTIONS = [
    "You are a pathology QA specialist for whole slide images.",
    "Go beyond pass/fail — diagnose root causes of quality issues.",
    "Provide actionable recommendations: re-scan, crop, flag for human.",
    "Detect systematic issues: scanner drift, staining inconsistency.",
    "When focus is low, determine if it's z-stack drift vs section quality.",
    "Support partial acceptance: identify usable regions even in failed slides.",
    "Track trends across studies to detect scanner degradation.",
    "Never approve slides that could compromise patient safety.",
]


def create_qa_agent(model_config: AgentModelConfig | None = None) -> Agent:
    """Create the QA specialist agent.

    Args:
        model_config: Model configuration. Defaults to cloud config.

    Returns:
        Configured Agno Agent instance.
    """
    from wsi_py_ai.agents.config import AgentModelConfig

    config = model_config or AgentModelConfig()

    return Agent(
        model=Claude(id=config.qa),
        name=AgentRole.QA.value,
        description="WSI Quality Assessment Specialist — diagnoses issues and recommends actions",
        instructions=QA_INSTRUCTIONS,
        tools=[qa_assess, qa_batch],
    )


QAAgent = create_qa_agent
