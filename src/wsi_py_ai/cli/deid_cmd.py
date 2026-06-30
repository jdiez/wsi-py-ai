"""CLI commands for de-identification."""

import typer

deid_app = typer.Typer(help="De-identify slides")


@deid_app.command("run")
def deid_run(
    slide_id: str = typer.Argument(..., help="Slide ID to de-identify"),
) -> None:
    """De-identify a single slide."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig
    from wsi_py_ai.deid.deidentifier import WSIDeidentifier

    config = WSIPipelineConfig()
    backends = get_backends(config)
    deid = WSIDeidentifier(backends=backends, salt=config.deid_salt)
    result = deid.deidentify(slide_id)
    typer.echo(f"De-identified: {result.slide_id} → {result.clean_uri}")


@deid_app.command("batch")
def deid_batch(
    study: str = typer.Option(..., "--study", help="Study identifier"),
    parallel: int = typer.Option(4, "--parallel", help="Number of parallel workers"),
) -> None:
    """Batch de-identification for a study."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig
    from wsi_py_ai.deid.deidentifier import WSIDeidentifier

    config = WSIPipelineConfig()
    backends = get_backends(config)
    deid = WSIDeidentifier(backends=backends, salt=config.deid_salt)
    results = deid.batch_deidentify(study, parallel)
    typer.echo(f"De-identified {len(results)} slides in study {study}")
