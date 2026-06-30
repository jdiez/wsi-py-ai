"""Local on-premise backend implementations."""

from __future__ import annotations

import os
import shutil
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

import structlog

from wsi_py_ai.backends.base import ComputeBackend, InferenceBackend, RegistryBackend, StorageBackend

logger: structlog.stdlib.BoundLogger = structlog.get_logger("wsi_py_ai.backends.local")


class LocalStorageBackend(StorageBackend):
    """Filesystem-based storage backend."""

    def __init__(self, base_dir: Path) -> None:
        """Initialize local storage.

        Args:
            base_dir: Root directory for file storage.
        """
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def upload(self, local_path: Path, remote_key: str) -> str:
        """Copy a local file into the managed storage directory.

        Args:
            local_path: Source file path.
            remote_key: Relative destination path within base_dir.

        Returns:
            Absolute path of the stored file.
        """
        dest = self.base_dir / remote_key
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(local_path, dest)
        logger.info("file.uploaded", source=str(local_path), dest=str(dest))
        return str(dest)

    def download(self, remote_key: str, local_path: Path) -> Path:
        """Copy a file from managed storage to a local path.

        Args:
            remote_key: Relative source path within base_dir.
            local_path: Destination path.

        Returns:
            The destination path.
        """
        source = self.base_dir / remote_key
        local_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, local_path)
        return local_path

    def list_files(self, prefix: str, pattern: str = "*") -> Iterator[str]:
        """List files under prefix matching pattern.

        Args:
            prefix: Directory prefix to search.
            pattern: Glob pattern for filtering.

        Yields:
            Relative paths of matching files.
        """
        search_dir = self.base_dir / prefix
        if search_dir.is_dir():
            for path in search_dir.rglob(pattern):
                if path.is_file():
                    yield str(path.relative_to(self.base_dir))

    def exists(self, key: str) -> bool:
        """Check if a file exists in local storage.

        Args:
            key: Relative path to check.

        Returns:
            True if file exists.
        """
        return (self.base_dir / key).exists()


class SQLiteRegistryBackend(RegistryBackend):
    """SQLite-based registry backend for single-user or small-team use."""

    def __init__(self, db_path: Path) -> None:
        """Initialize SQLite registry.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Create the slides table if it doesn't exist."""
        import sqlite3

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS slides (
                    slide_id TEXT PRIMARY KEY,
                    metadata TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def register_slide(self, slide_id: str, metadata: dict[str, Any]) -> None:
        """Register a slide in SQLite.

        Args:
            slide_id: Unique slide identifier.
            metadata: Slide metadata to store as JSON.
        """
        import json
        import sqlite3

        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO slides (slide_id, metadata, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (slide_id, json.dumps(metadata)),
            )
            conn.commit()
        logger.info("slide.registered", slide_id=slide_id)

    def query(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        """Query slides from SQLite by metadata filters.

        Args:
            filters: Key-value pairs to match against stored metadata.

        Returns:
            List of matching slide metadata dictionaries.
        """
        import json
        import sqlite3

        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("SELECT slide_id, metadata FROM slides")
            results: list[dict[str, Any]] = []
            for row in cursor:
                meta: dict[str, Any] = json.loads(row[1])
                if all(meta.get(k) == v for k, v in filters.items()):
                    results.append({"slide_id": row[0], **meta})
            return results

    def update(self, slide_id: str, fields: dict[str, Any]) -> None:
        """Update metadata fields for a slide.

        Args:
            slide_id: Slide to update.
            fields: Fields to merge into existing metadata.
        """
        import json
        import sqlite3

        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.execute("SELECT metadata FROM slides WHERE slide_id = ?", (slide_id,))
            row = cursor.fetchone()
            if row is None:
                msg = f"Slide {slide_id} not found"
                raise ValueError(msg)
            meta: dict[str, Any] = json.loads(row[0])
            meta.update(fields)
            conn.execute(
                "UPDATE slides SET metadata = ?, updated_at = CURRENT_TIMESTAMP WHERE slide_id = ?",
                (json.dumps(meta), slide_id),
            )
            conn.commit()


class LocalComputeBackend(ComputeBackend):
    """Multiprocessing-based compute backend."""

    def run_batch(self, fn: Any, items: list[Any], max_workers: int = 4) -> list[Any]:
        """Run function over items using ProcessPoolExecutor.

        Args:
            fn: Callable to apply.
            items: Items to process.
            max_workers: Number of parallel processes.

        Returns:
            List of results.
        """
        effective_workers = min(max_workers, os.cpu_count() or 4)
        with ProcessPoolExecutor(max_workers=effective_workers) as pool:
            return list(pool.map(fn, items))


class LocalInferenceBackend(InferenceBackend):
    """Local GPU/CPU inference backend.

    Requires torch to be installed (optional dependency).
    """

    def __init__(self, models_dir: Path, device: str = "cpu") -> None:
        """Initialize local inference backend.

        Args:
            models_dir: Directory containing model weight files.
            device: Compute device (cuda, mps, cpu).
        """
        self.models_dir = models_dir
        self.device = device

    def predict(self, model_name: str, inputs: list[Any]) -> list[Any]:
        """Run local model prediction.

        Args:
            model_name: Name of the model (expects {model_name}.pt in models_dir).
            inputs: List of inputs.

        Returns:
            List of prediction outputs.

        Raises:
            NotImplementedError: Torch-based inference requires torch optional dep.
        """
        raise NotImplementedError("Local inference requires torch. Install with: uv add torch torchvision")
