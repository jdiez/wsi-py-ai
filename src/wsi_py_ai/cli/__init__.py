"""CLI entry point for the WSI pipeline."""

import typer

from wsi_py_ai.cli.agent_cmd import agent_app
from wsi_py_ai.cli.config_cmd import config_app
from wsi_py_ai.cli.dataloader_cmd import dataloader_app
from wsi_py_ai.cli.deid_cmd import deid_app
from wsi_py_ai.cli.ingest_cmd import ingest_app
from wsi_py_ai.cli.pipeline_cmd import pipeline_app
from wsi_py_ai.cli.qa_cmd import qa_app
from wsi_py_ai.cli.registry_cmd import registry_app

app = typer.Typer(name="wsi", help="WSI Processing Pipeline — local and cloud")

app.add_typer(ingest_app, name="ingest")
app.add_typer(deid_app, name="deid")
app.add_typer(registry_app, name="registry")
app.add_typer(dataloader_app, name="dataloader")
app.add_typer(qa_app, name="qa")
app.add_typer(pipeline_app, name="pipeline")
app.add_typer(config_app, name="config")
app.add_typer(agent_app, name="agent")


@app.callback()
def main(
    mode: str | None = typer.Option(None, "--mode", help="Backend mode: local or gcp"),
    config: str | None = typer.Option(None, "--config", help="Path to config file"),
) -> None:
    """WSI Processing Pipeline — works on local hardware or GCP."""
