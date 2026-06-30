"""Backend abstraction layer for dual-mode (local/GCP) operation."""

from wsi_py_ai.backends.base import ComputeBackend, InferenceBackend, RegistryBackend, StorageBackend
from wsi_py_ai.backends.factory import get_backends

__all__ = [
    "ComputeBackend",
    "InferenceBackend",
    "RegistryBackend",
    "StorageBackend",
    "get_backends",
]
