"""CLI commands for configuration management."""

import typer

config_app = typer.Typer(help="Configuration management")


@config_app.command("show")
def config_show() -> None:
    """Show current configuration."""
    from wsi_py_ai.config.settings import WSIPipelineConfig

    config = WSIPipelineConfig()
    typer.echo(f"Mode: {config.mode.value}")
    typer.echo(f"Region: {config.gcp_region}")
    if config.mode.value == "local":
        typer.echo(f"Base dir: {config.local_base_dir}")
        typer.echo(f"DB: {config.local_db}")
        typer.echo(f"Device: {config.local_device}")
    else:
        typer.echo(f"Project: {config.gcp_project}")
        typer.echo(f"Raw bucket: {config.raw_bucket}")
        typer.echo(f"Clean bucket: {config.clean_bucket}")


@config_app.command("check")
def config_check() -> None:
    """Validate configuration and connectivity."""
    from wsi_py_ai.config.settings import WSIPipelineConfig

    config = WSIPipelineConfig()
    typer.echo(f"Mode: {config.mode.value}")

    issues: list[str] = []
    if config.mode.value == "gcp" and not config.gcp_project:
        issues.append("GCP project not set (WSI_GCP_PROJECT)")
    if config.mode.value == "gcp" and not config.raw_bucket:
        issues.append("Raw bucket not set (WSI_RAW_BUCKET)")

    if issues:
        typer.echo("Issues found:")
        for issue in issues:
            typer.echo(f"  ✗ {issue}")
        raise typer.Exit(code=1)

    typer.echo("Configuration valid.")
