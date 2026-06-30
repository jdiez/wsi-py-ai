"""Registry agent — manages dataset curation and metadata."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agno.agent import Agent
from agno.models.anthropic import Claude

from wsi_py_ai.agents.base import AgentRole
from wsi_py_ai.tools.registry_tools import registry_query, registry_register, registry_version_create

if TYPE_CHECKING:
    from wsi_py_ai.agents.config import AgentModelConfig

REGISTRY_INSTRUCTIONS = [
    "You manage WSI dataset curation and metadata enrichment.",
    "Enrich metadata from filename patterns, DICOM tags, and study context.",
    "Detect and resolve conflicts — same patient, different study IDs.",
    "Validate dataset cohesion for ML training (stain balance, organ coverage).",
    "Create reproducible dataset versions with provenance tracking.",
    "Surface data gaps that would bias downstream models.",
    "Maintain FAIR principles (Findable, Accessible, Interoperable, Reusable).",
]


def create_registry_agent(model_config: AgentModelConfig | None = None) -> Agent:
    """Create the registry/curation specialist agent.

    Args:
        model_config: Model configuration. Defaults to cloud config.

    Returns:
        Configured Agno Agent instance.
    """
    from wsi_py_ai.agents.config import AgentModelConfig

    config = model_config or AgentModelConfig()

    return Agent(
        model=Claude(id=config.registry),
        name=AgentRole.REGISTRY.value,
        description="WSI Registry Specialist — curates datasets and enriches metadata",
        instructions=REGISTRY_INSTRUCTIONS,
        tools=[registry_query, registry_register, registry_version_create],
    )


RegistryAgent = create_registry_agent
