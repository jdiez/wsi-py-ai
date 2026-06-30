"""Recovery agent — diagnoses failures and orchestrates retries."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agno.agent import Agent
from agno.models.anthropic import Claude

from wsi_py_ai.agents.base import AgentRole
from wsi_py_ai.tools.ingest_tools import ingest_file
from wsi_py_ai.tools.qa_tools import qa_assess

if TYPE_CHECKING:
    from wsi_py_ai.agents.config import AgentModelConfig

RECOVERY_INSTRUCTIONS = [
    "You diagnose pipeline failures and orchestrate recovery.",
    "Categorize failures: transient (retry), permanent (skip + alert), unknown (escalate).",
    "Track failure patterns to detect systematic issues (e.g. scanner offline).",
    "Implement exponential backoff with jitter for transient failures.",
    "Quarantine problematic slides rather than blocking the whole pipeline.",
    "Generate incident reports for repeated failures.",
    "Never retry de-identification failures without human review.",
]


def create_recovery_agent(model_config: AgentModelConfig | None = None) -> Agent:
    """Create the recovery/error-handling specialist agent.

    Args:
        model_config: Model configuration. Defaults to cloud config.

    Returns:
        Configured Agno Agent instance.
    """
    from wsi_py_ai.agents.config import AgentModelConfig

    config = model_config or AgentModelConfig()

    return Agent(
        model=Claude(id=config.recovery),
        name=AgentRole.RECOVERY.value,
        description="WSI Recovery Specialist — diagnoses failures and retries intelligently",
        instructions=RECOVERY_INSTRUCTIONS,
        tools=[ingest_file, qa_assess],
    )


RecoveryAgent = create_recovery_agent
