"""Abstract base classes for backend interfaces."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any


class StorageBackend(ABC):
    """Abstract storage backend for WSI files."""

    @abstractmethod
    def upload(self, local_path: Path, remote_key: str) -> str:
        """Upload a local file to storage.

        Args:
            local_path: Path to the local file.
            remote_key: Destination key/path in storage.

        Returns:
            The storage URI of the uploaded file.
        """

    @abstractmethod
    def download(self, remote_key: str, local_path: Path) -> Path:
        """Download a file from storage to local path.

        Args:
            remote_key: Source key/path in storage.
            local_path: Local destination path.

        Returns:
            The local path where the file was downloaded.
        """

    @abstractmethod
    def list_files(self, prefix: str, pattern: str = "*") -> Iterator[str]:
        """List files in storage matching a prefix and pattern.

        Args:
            prefix: Storage prefix to search under.
            pattern: Glob pattern to filter files.

        Yields:
            Storage keys matching the criteria.
        """

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if a file exists in storage.

        Args:
            key: Storage key to check.

        Returns:
            True if the file exists.
        """


class RegistryBackend(ABC):
    """Abstract registry backend for slide metadata."""

    @abstractmethod
    def register_slide(self, slide_id: str, metadata: dict[str, Any]) -> None:
        """Register a slide in the catalog.

        Args:
            slide_id: Unique slide identifier.
            metadata: Slide metadata dictionary.
        """

    @abstractmethod
    def query(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        """Query slides matching filters.

        Args:
            filters: Key-value pairs to filter by.

        Returns:
            List of slide metadata dictionaries matching the query.
        """

    @abstractmethod
    def update(self, slide_id: str, fields: dict[str, Any]) -> None:
        """Update fields for a registered slide.

        Args:
            slide_id: Unique slide identifier.
            fields: Fields to update.
        """


class ComputeBackend(ABC):
    """Abstract compute backend for parallel processing."""

    @abstractmethod
    def run_batch(self, fn: Any, items: list[Any], max_workers: int = 4) -> list[Any]:
        """Run a function over items in parallel.

        Args:
            fn: Callable to apply to each item.
            items: Items to process.
            max_workers: Maximum parallel workers.

        Returns:
            Results from processing each item.
        """


class InferenceBackend(ABC):
    """Abstract inference backend for ML model predictions."""

    @abstractmethod
    def predict(self, model_name: str, inputs: list[Any]) -> list[Any]:
        """Run predictions on inputs using a named model.

        Args:
            model_name: Name of the model to use.
            inputs: List of inputs for prediction.

        Returns:
            List of prediction results.
        """
