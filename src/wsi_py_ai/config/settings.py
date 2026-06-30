"""Pipeline configuration with dual-mode support (local/GCP)."""

from enum import Enum

from pydantic_settings import BaseSettings


class BackendMode(str, Enum):
    """Backend execution mode."""

    LOCAL = "local"
    GCP = "gcp"


class WSIPipelineConfig(BaseSettings):
    """WSI Pipeline configuration — environment-driven, dual-mode.

    All settings can be overridden via environment variables prefixed with WSI_.
    Example: WSI_MODE=gcp, WSI_GCP_PROJECT=my-project.

    Attributes:
        mode: Backend mode (local or gcp).
        local_base_dir: Root directory for local file storage.
        local_db: SQLite or PostgreSQL connection string for local registry.
        local_models_dir: Directory for local QA model weights.
        local_device: Compute device for local inference (cuda, mps, cpu).
        local_max_workers: Default parallel workers for local processing.
        gcp_project: GCP project ID (required for gcp mode).
        gcp_region: GCP region for Dataflow and Vertex AI.
        raw_bucket: GCS bucket for raw ingested slides.
        clean_bucket: GCS bucket for de-identified slides.
        tiles_bucket: GCS bucket for pre-tiled patches.
        registry_dataset: BigQuery dataset name for slide registry.
        registry_table: BigQuery table name for slides.
        deid_salt_secret: Secret Manager path for de-identification salt.
        qa_endpoint: Vertex AI endpoint for QA model.
        deid_salt: Direct salt value for local mode.
        qa_thresholds_focus: Minimum focus score for QA pass.
        qa_thresholds_coverage: Minimum tissue coverage for QA pass.
        qa_thresholds_artifacts: Maximum artifact percentage for QA pass.
        qa_thresholds_stain: Minimum stain uniformity for QA pass.
    """

    mode: BackendMode = BackendMode.LOCAL

    # Local settings
    local_base_dir: str = "/data/wsi-pipeline"
    local_db: str = "/data/wsi-pipeline/registry.db"
    local_models_dir: str = "/data/wsi-pipeline/models"
    local_device: str = "cpu"
    local_max_workers: int = 4

    # GCP settings
    gcp_project: str = ""
    gcp_region: str = "us-central1"
    raw_bucket: str = ""
    clean_bucket: str = ""
    tiles_bucket: str = ""
    registry_dataset: str = "wsi_registry"
    registry_table: str = "slides"
    deid_salt_secret: str = ""
    qa_endpoint: str = ""

    # Shared settings
    deid_salt: str = ""
    qa_thresholds_focus: float = 0.7
    qa_thresholds_coverage: float = 0.3
    qa_thresholds_artifacts: float = 0.15
    qa_thresholds_stain: float = 0.6

    model_config = {"env_prefix": "WSI_", "env_file": ".env"}
