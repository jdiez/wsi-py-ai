"""Tests for backend implementations."""

import tempfile
from pathlib import Path

from wsi_py_ai.backends.local import LocalComputeBackend, LocalStorageBackend, SQLiteRegistryBackend


def test_local_storage_upload_and_exists():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = LocalStorageBackend(Path(tmpdir))
        source = Path(tmpdir) / "source.txt"
        source.write_text("test content")

        uri = storage.upload(source, "study/slide.txt")
        assert storage.exists("study/slide.txt")
        assert Path(uri).read_text() == "test content"


def test_local_storage_list_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = LocalStorageBackend(Path(tmpdir))
        (Path(tmpdir) / "study").mkdir()
        (Path(tmpdir) / "study" / "a.svs").write_text("a")
        (Path(tmpdir) / "study" / "b.svs").write_text("b")

        files = list(storage.list_files("study", "*.svs"))
        assert len(files) == 2


def test_sqlite_registry_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        registry = SQLiteRegistryBackend(db_path)

        registry.register_slide("SLIDE-001", {"study_id": "STUDY-1", "tissue": "prostate"})
        results = registry.query({"study_id": "STUDY-1"})
        assert len(results) == 1
        assert results[0]["slide_id"] == "SLIDE-001"
        assert results[0]["tissue"] == "prostate"


def test_sqlite_registry_update():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        registry = SQLiteRegistryBackend(db_path)

        registry.register_slide("SLIDE-001", {"study_id": "ST1", "status": "raw"})
        registry.update("SLIDE-001", {"status": "clean", "qa_passed": True})
        results = registry.query({"study_id": "ST1"})
        assert results[0]["status"] == "clean"
        assert results[0]["qa_passed"] is True


def _double(x: int) -> int:
    return x * 2


def test_local_compute_batch():
    compute = LocalComputeBackend()
    results = compute.run_batch(_double, [1, 2, 3], max_workers=2)
    assert results == [2, 4, 6]
