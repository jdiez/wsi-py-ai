"""CLI commands for WSI ingestion."""

import typer

ingest_app = typer.Typer(help="Ingest WSI files")


@ingest_app.command("file")
def ingest_file(
    path: str = typer.Argument(..., help="Path to WSI file"),
    study: str = typer.Option(..., "--study", help="Study identifier"),
) -> None:
    """Ingest a single WSI file."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig
    from wsi_py_ai.ingest.ingester import WSIIngester

    config = WSIPipelineConfig()
    backends = get_backends(config)
    ingester = WSIIngester(backends=backends)
    result = ingester.ingest(path, study)
    typer.echo(f"Ingested: {result.slide_id} → {result.storage_uri}")


@ingest_app.command("dir")
def ingest_dir(
    path: str = typer.Argument(..., help="Directory containing WSI files"),
    study: str = typer.Option(..., "--study", help="Study identifier"),
    pattern: str = typer.Option("*", "--pattern", help="Glob pattern for files"),
    parallel: int = typer.Option(4, "--parallel", help="Number of parallel workers"),
) -> None:
    """Ingest all WSI files from a directory."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig
    from wsi_py_ai.ingest.ingester import WSIIngester

    config = WSIPipelineConfig()
    backends = get_backends(config)
    ingester = WSIIngester(backends=backends)
    results = ingester.batch_ingest(path, study, pattern, parallel)
    typer.echo(f"Ingested {len(results)} slides into study {study}")
