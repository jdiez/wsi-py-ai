"""CLI subcommand for the multi-agent system."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

agent_app = typer.Typer(help="Multi-agent pipeline orchestration")

_DEFAULT_AUDIT_DIR = Path("./audit")


@agent_app.command("run")
def agent_run(
    goal: Annotated[str, typer.Argument(help="Natural language goal for the agent team")],
    model_config: Annotated[str | None, typer.Option("--model-config", help="Model config: 'cloud' or 'local'")] = None,
    audit_dir: Annotated[
        Path, typer.Option("--audit-dir", help="Directory for decision audit logs")
    ] = _DEFAULT_AUDIT_DIR,
) -> None:
    """Run the multi-agent planner with a natural language goal."""
    from wsi_py_ai.agents.config import AgentModelConfig, LocalAgentModelConfig
    from wsi_py_ai.agents.planner import create_planner_agent

    config = LocalAgentModelConfig() if model_config == "local" else AgentModelConfig()
    agent = create_planner_agent(model_config=config)

    typer.echo(f"Running agent with goal: {goal}")
    typer.echo(f"Model config: {type(config).__name__}")
    typer.echo(f"Audit dir: {audit_dir}")
    response = agent.run(goal)
    typer.echo(f"\nAgent response:\n{response.content}")


@agent_app.command("status")
def agent_status() -> None:
    """Show current agent system configuration."""
    from wsi_py_ai.agents.config import AgentModelConfig
    from wsi_py_ai.orchestration.guardrails import AgentGuardrails

    config = AgentModelConfig()
    guardrails = AgentGuardrails()

    typer.echo("Agent Model Configuration:")
    for field, value in config.model_dump().items():
        typer.echo(f"  {field}: {value}")

    typer.echo("\nGuardrails:")
    for field, value in guardrails.model_dump().items():
        typer.echo(f"  {field}: {value}")
