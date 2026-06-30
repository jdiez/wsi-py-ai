"""De-identification agent — ensures complete PHI removal."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agno.agent import Agent
from agno.models.anthropic import Claude

from wsi_py_ai.agents.base import AgentRole
from wsi_py_ai.tools.deid_tools import deid_batch, deid_run

if TYPE_CHECKING:
    from wsi_py_ai.agents.config import AgentModelConfig

DEID_INSTRUCTIONS = [
    "You ensure complete removal of Protected Health Information (PHI) from WSI files.",
    "Verify de-identification completeness — re-run OCR post-redaction to confirm no text remains.",
    "Handle institution-specific metadata formats not covered by standard DICOM profiles.",
    "Flag uncertain cases conservatively — when in doubt, escalate to human.",
    "Detect PHI in unexpected locations: free-text comments, custom DICOM private tags.",
    "Never skip de-identification for any reason — PHI compliance is non-negotiable.",
    "Log all decisions for regulatory audit trail.",
]


def create_deid_agent(model_config: AgentModelConfig | None = None) -> Agent:
    """Create the de-identification specialist agent.

    Args:
        model_config: Model configuration. Defaults to cloud config.

    Returns:
        Configured Agno Agent instance.
    """
    from wsi_py_ai.agents.config import AgentModelConfig

    config = model_config or AgentModelConfig()

    return Agent(
        model=Claude(id=config.deid),
        name=AgentRole.DEID.value,
        description="WSI De-identification Specialist — verifies complete PHI removal",
        instructions=DEID_INSTRUCTIONS,
        tools=[deid_run, deid_batch],
    )


DeidAgent = create_deid_agent
