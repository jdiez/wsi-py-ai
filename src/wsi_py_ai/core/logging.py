"""Structured logging configuration."""

import structlog

logger: structlog.stdlib.BoundLogger = structlog.get_logger("wsi_py_ai")
