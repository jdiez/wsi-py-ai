"""Training agent — optimizes data loading for ML workflows."""

from __future__ import annotations

from typing import TYPE_CHECKING

from agno.agent import Agent
from agno.models.anthropic import Claude

from wsi_py_ai.agents.base import AgentRole
from wsi_py_ai.tools.dataloader_tools import dataloader_pretile, dataloader_stream

if TYPE_CHECKING:
    from wsi_py_ai.agents.config import AgentModelConfig

TRAINING_INSTRUCTIONS = [
    "You optimize WSI data loading and tiling for ML training workflows.",
    "Recommend tile sizes and overlap based on model architecture.",
    "Balance cache vs compute tradeoffs for different hardware.",
    "Handle class imbalance — oversample rare stains and pathologies.",
    "Monitor data pipeline throughput and identify bottlenecks.",
    "Adapt strategies for different training phases (pretrain, finetune, eval).",
    "Ensure reproducibility with deterministic tiling seeds.",
]


def create_training_agent(model_config: AgentModelConfig | None = None) -> Agent:
    """Create the training/dataloader specialist agent.

    Args:
        model_config: Model configuration. Defaults to cloud config.

    Returns:
        Configured Agno Agent instance.
    """
    from wsi_py_ai.agents.config import AgentModelConfig

    config = model_config or AgentModelConfig()

    return Agent(
        model=Claude(id=config.training),
        name=AgentRole.TRAINING.value,
        description="WSI Training Specialist — optimizes data loading for ML workflows",
        instructions=TRAINING_INSTRUCTIONS,
        tools=[dataloader_pretile, dataloader_stream],
    )


TrainingAgent = create_training_agent
