"""Tests for WSI pipeline configuration."""

from wsi_py_ai.config.settings import BackendMode, WSIPipelineConfig


def test_default_config_is_local():
    config = WSIPipelineConfig()
    assert config.mode == BackendMode.LOCAL


def test_local_config_has_defaults():
    config = WSIPipelineConfig()
    assert config.local_base_dir == "/data/wsi-pipeline"
    assert config.local_device == "cpu"
    assert config.local_max_workers == 4


def test_qa_thresholds_defaults():
    config = WSIPipelineConfig()
    assert config.qa_thresholds_focus == 0.7
    assert config.qa_thresholds_coverage == 0.3
    assert config.qa_thresholds_artifacts == 0.15
    assert config.qa_thresholds_stain == 0.6
