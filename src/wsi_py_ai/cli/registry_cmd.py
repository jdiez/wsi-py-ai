"""CLI commands for dataset registry."""

import typer

registry_app = typer.Typer(help="Dataset registry operations")


@registry_app.command("query")
def registry_query(
    tissue: str | None = typer.Option(None, "--tissue", help="Filter by tissue type"),
    stain: str | None = typer.Option(None, "--stain", help="Filter by stain type"),
    qa_passed: bool | None = typer.Option(None, "--qa-passed", help="Filter by QA status"),
    study: str | None = typer.Option(None, "--study", help="Filter by study ID"),
) -> None:
    """Query the slide registry."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig
    from wsi_py_ai.registry.registry import DatasetRegistry

    config = WSIPipelineConfig()
    backends = get_backends(config)
    registry = DatasetRegistry(backends=backends)
    results = registry.query(tissue_type=tissue, stain=stain, qa_passed=qa_passed, study_id=study)
    typer.echo(f"Found {len(results)} slides")
    for slide in results[:10]:
        typer.echo(f"  {slide.get('slide_id', 'unknown')} — {slide.get('tissue_type', '?')}")


@registry_app.command("version")
def registry_version(
    name: str = typer.Argument(..., help="Version name"),
    query: str = typer.Option("", "--query", help="Filter query"),
    split: str = typer.Option("train:0.7,val:0.15,test:0.15", "--split", help="Split ratios"),
) -> None:
    """Create a versioned dataset."""
    from wsi_py_ai.backends.factory import get_backends
    from wsi_py_ai.config.settings import WSIPipelineConfig
    from wsi_py_ai.registry.registry import DatasetRegistry

    config = WSIPipelineConfig()
    backends = get_backends(config)
    registry = DatasetRegistry(backends=backends)

    splits = {}
    for part in split.split(","):
        key, val = part.split(":")
        splits[key.strip()] = float(val.strip())

    version = registry.create_version(name=name, query=query, splits=splits)
    typer.echo(f"Created version '{version.name}' with {len(version.slide_ids)} slides")
