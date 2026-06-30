"""Backend factory for constructing backend instances from configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wsi_py_ai.config.settings import WSIPipelineConfig


def get_backends(config: WSIPipelineConfig) -> dict[str, Any]:
    """Create backend instances based on configuration mode.

    Args:
        config: Pipeline configuration with mode and connection details.

    Returns:
        Dictionary with keys: storage, registry, compute, inference.

    Raises:
        ValueError: If mode is not recognized.
    """
    from pathlib import Path

    from wsi_py_ai.config.settings import BackendMode

    if config.mode == BackendMode.LOCAL:
        from wsi_py_ai.backends.local import (
            LocalComputeBackend,
            LocalInferenceBackend,
            LocalStorageBackend,
            SQLiteRegistryBackend,
        )

        base_dir = Path(config.local_base_dir)
        return {
            "storage": LocalStorageBackend(base_dir),
            "registry": SQLiteRegistryBackend(Path(config.local_db)),
            "compute": LocalComputeBackend(),
            "inference": LocalInferenceBackend(Path(config.local_models_dir), config.local_device),
        }

    if config.mode == BackendMode.GCP:
        from wsi_py_ai.backends.gcp import (
            BigQueryRegistryBackend,
            DataflowComputeBackend,
            GCSStorageBackend,
            VertexInferenceBackend,
        )

        return {
            "storage": GCSStorageBackend(config.gcp_project, config.raw_bucket),
            "registry": BigQueryRegistryBackend(config.gcp_project, config.registry_dataset),
            "compute": DataflowComputeBackend(config.gcp_project, config.gcp_region),
            "inference": VertexInferenceBackend(config.gcp_project, config.qa_endpoint),
        }

    msg = f"Unknown backend mode: {config.mode}"
    raise ValueError(msg)
