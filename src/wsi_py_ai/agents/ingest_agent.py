"""Ingest agent — handles complex ingestion scenarios."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agno.agent import Agent
from agno.models.anthropic import Claude

from wsi_py_ai.agents.base import AgentRole
from wsi_py_ai.tools.ingest_tools import ingest_batch, ingest_file

if TYPE_CHECKING:
    from wsi_py_ai.agents.config import AgentModelConfig

INGEST_INSTRUCTIONS = [
    "You handle complex WSI file ingestion scenarios.",
    "Detect file formats when extension is wrong or missing.",
    "Handle corrupted files: attempt partial read, log corruption details.",
    "Detect duplicates — same slide scanned at different times.",
    "Manage source unavailability with retry scheduling.",
    "Validate file integrity (checksum, header parse) before committing.",
    "Report detailed ingestion metrics per batch.",
]


def create_ingest_agent(model_config: AgentModelConfig | None = None) -> Agent:
    """Create the ingestion specialist agent.

    Args:
        model_config: Model configuration. Defaults to cloud config.

    Returns:
        Configured Agno Agent instance.
    """
    from wsi_py_ai.agents.config import AgentModelConfig

    config = model_config or AgentModelConfig()

    return Agent(
        model=Claude(id=config.ingest),
        name=AgentRole.INGEST.value,
        description="WSI Ingestion Specialist — handles format detection and edge cases",
        instructions=INGEST_INSTRUCTIONS,
        tools=[ingest_file, ingest_batch],
    )


IngestAgent = create_ingest_agent
