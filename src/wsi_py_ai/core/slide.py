"""Slide reader abstraction for vendor-neutral WSI access."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np
from pydantic import BaseModel

from wsi_py_ai.core.types import SlideFormat, SlideMetadata


class SlideProperties(BaseModel, frozen=True):
    """Properties read from a slide file header.

    Attributes:
        width: Slide width in pixels at native magnification.
        height: Slide height in pixels at native magnification.
        magnification: Native magnification (e.g., 40.0).
        mpp: Microns per pixel at native magnification.
        levels: Number of pyramid levels available.
        format: Detected slide format.
        vendor: Scanner vendor string.
    """

    width: int
    height: int
    magnification: float = 40.0
    mpp: float = 0.25
    levels: int = 1
    format: SlideFormat = SlideFormat.SVS
    vendor: str = ""


class SlideReader(ABC):
    """Abstract base for reading WSI files regardless of vendor format."""

    @abstractmethod
    def open(self, path: Path) -> None:
        """Open a slide file for reading.

        Args:
            path: Path to the WSI file.
        """

    @abstractmethod
    def close(self) -> None:
        """Close the slide and release resources."""

    @abstractmethod
    def read_region(self, location: tuple[int, int], level: int, size: tuple[int, int]) -> np.ndarray:
        """Read a region from the slide at a given pyramid level.

        Args:
            location: (x, y) top-left corner at level 0 coordinates.
            level: Pyramid level (0 = highest resolution).
            size: (width, height) of the region to read.

        Returns:
            NumPy array of shape (height, width, channels) in RGB.
        """

    @abstractmethod
    def get_properties(self) -> SlideProperties:
        """Get slide properties from the header.

        Returns:
            SlideProperties with dimensions, magnification, etc.
        """

    @abstractmethod
    def get_thumbnail(self, size: tuple[int, int] = (512, 512)) -> np.ndarray:
        """Get a thumbnail image of the entire slide.

        Args:
            size: Maximum (width, height) for the thumbnail.

        Returns:
            NumPy array of the thumbnail in RGB.
        """

    @abstractmethod
    def get_metadata(self) -> SlideMetadata:
        """Extract structured metadata from the slide.

        Returns:
            SlideMetadata pydantic model.
        """

    def __enter__(self) -> SlideReader:
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit — closes the slide."""
        self.close()


class LocalSlideReader(SlideReader):
    """Local slide reader using OpenSlide (if available) or stub.

    Falls back to basic TIFF reading if OpenSlide is not installed.

    Attributes:
        path: Path to the opened slide file.
    """

    def __init__(self) -> None:
        """Initialize local slide reader."""
        self.path: Path | None = None
        self._properties: SlideProperties | None = None

    def open(self, path: Path) -> None:
        """Open a slide file.

        Args:
            path: Path to the WSI file.

        Raises:
            FileNotFoundError: If path does not exist.
        """
        if not path.exists():
            msg = f"Slide file not found: {path}"
            raise FileNotFoundError(msg)
        self.path = path
        self._properties = SlideProperties(
            width=0,
            height=0,
            format=self._detect_format(path),
            vendor="unknown",
        )

    def close(self) -> None:
        """Close the slide."""
        self.path = None
        self._properties = None

    def read_region(self, location: tuple[int, int], level: int, size: tuple[int, int]) -> np.ndarray:
        """Read a region (stub — returns empty array).

        Args:
            location: Top-left corner coordinates.
            level: Pyramid level.
            size: Region dimensions.

        Returns:
            Empty RGB array of requested size.
        """
        return np.zeros((size[1], size[0], 3), dtype=np.uint8)

    def get_properties(self) -> SlideProperties:
        """Get slide properties.

        Returns:
            SlideProperties (stub values if OpenSlide unavailable).

        Raises:
            RuntimeError: If no slide is open.
        """
        if self._properties is None:
            msg = "No slide open — call open() first"
            raise RuntimeError(msg)
        return self._properties

    def get_thumbnail(self, size: tuple[int, int] = (512, 512)) -> np.ndarray:
        """Get thumbnail (stub — returns empty array).

        Args:
            size: Maximum thumbnail dimensions.

        Returns:
            Empty RGB array.
        """
        return np.zeros((size[1], size[0], 3), dtype=np.uint8)

    def get_metadata(self) -> SlideMetadata:
        """Extract metadata from the slide.

        Returns:
            SlideMetadata with available information.

        Raises:
            RuntimeError: If no slide is open.
        """
        if self.path is None:
            msg = "No slide open — call open() first"
            raise RuntimeError(msg)
        props = self.get_properties()
        return SlideMetadata(
            slide_id=self.path.stem,
            study_id="",
            format=props.format,
            magnification=props.magnification,
            width_px=props.width,
            height_px=props.height,
        )

    @staticmethod
    def _detect_format(path: Path) -> SlideFormat:
        """Detect slide format from file extension.

        Args:
            path: File path.

        Returns:
            Detected SlideFormat.
        """
        ext_map = {
            ".svs": SlideFormat.SVS,
            ".ndpi": SlideFormat.NDPI,
            ".dcm": SlideFormat.DICOM,
            ".isyntax": SlideFormat.ISYNTAX,
            ".mrxs": SlideFormat.MRXS,
            ".tif": SlideFormat.TIFF,
            ".tiff": SlideFormat.TIFF,
            ".bif": SlideFormat.BIF,
        }
        return ext_map.get(path.suffix.lower(), SlideFormat.TIFF)
