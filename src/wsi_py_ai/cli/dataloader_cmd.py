"""CLI commands for DataLoader operations."""

import typer

dataloader_app = typer.Typer(help="DataLoader and tiling")


@dataloader_app.command("pretile")
def dataloader_pretile(
    version: str = typer.Argument(..., help="Dataset version to tile"),
    tile_size: int = typer.Option(256, "--tile-size", help="Tile dimensions in pixels"),
    magnification: float = typer.Option(20.0, "--magnification", help="Target magnification"),
    tissue_threshold: float = typer.Option(0.5, "--tissue-threshold", help="Min tissue fraction"),
    output_format: str = typer.Option("webdataset", "--format", help="Output format"),
    parallel: int = typer.Option(4, "--parallel", help="Number of parallel workers"),
) -> None:
    """Pre-tile a dataset version for training speed."""
    from wsi_py_ai.dataloader.loader import TilingConfig, pretile_dataset

    tiling = TilingConfig(
        tile_size=tile_size,
        magnification=magnification,
        tissue_threshold=tissue_threshold,
    )
    pretile_dataset(
        registry_version=version,
        output_format=output_format,
        tiling=tiling,
        max_workers=parallel,
    )
    typer.echo(f"Pre-tiling complete for {version}")


@dataloader_app.command("stats")
def dataloader_stats(
    version: str = typer.Argument(..., help="Dataset version"),
) -> None:
    """Show tiling statistics for a dataset version."""
    typer.echo(f"Statistics for version: {version}")
    typer.echo("  (not yet implemented — requires tiled data)")
