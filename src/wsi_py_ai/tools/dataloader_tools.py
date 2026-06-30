"""Agno tools wrapping the WSI dataloader module."""

from __future__ import annotations

import json

from agno.tools.decorator import tool

from wsi_py_ai.dataloader.loader import TilingConfig, WSIDataLoader, pretile_dataset


@tool
def dataloader_pretile(registry_version: str, tile_size: int = 256, overlap: int = 0) -> str:
    """Pre-tile all slides in a dataset version for ML training.

    Args:
        registry_version: Dataset version name to tile.
        tile_size: Tile dimension in pixels (default: 256).
        overlap: Overlap between adjacent tiles in pixels (default: 0).

    Returns:
        JSON string with tiling configuration used.
    """
    tiling = TilingConfig(tile_size=tile_size, overlap=overlap)
    pretile_dataset(registry_version=registry_version, tiling=tiling)
    return json.dumps({
        "status": "pretiled",
        "registry_version": registry_version,
        "tile_size": tile_size,
        "overlap": overlap,
    })


@tool
def dataloader_stream(registry_version: str, batch_size: int = 32, tile_size: int = 256) -> str:
    """Configure a streaming dataloader for ML training.

    Args:
        registry_version: Dataset version name to load.
        batch_size: Number of tiles per batch (default: 32).
        tile_size: Tile dimension in pixels (default: 256).

    Returns:
        JSON string with dataloader configuration details.
    """
    tiling = TilingConfig(tile_size=tile_size)
    loader = WSIDataLoader(registry_version=registry_version, batch_size=batch_size, tiling=tiling)
    return json.dumps({
        "status": "configured",
        "registry_version": loader.registry_version,
        "batch_size": loader.batch_size,
        "tile_size": loader.tiling.tile_size,
        "num_workers": loader.num_workers,
    })
