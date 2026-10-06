"""Laden von Kamerabildern als float-Array (Graustufen)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

IMAGE_SUFFIXES = (".bmp", ".png", ".tif", ".tiff", ".jpg", ".jpeg")


def is_image_file(path: str | Path) -> bool:
    return Path(path).suffix.lower() in IMAGE_SUFFIXES


def is_background_file(path: str | Path) -> bool:
    """Dateien mit 'background'/'hintergrund' im Namen werden im Batch uebersprungen."""
    name = Path(path).stem.lower()
    return "background" in name or "hintergrund" in name


def load_image(path: str | Path) -> tuple[np.ndarray, float]:
    """Laedt ein Bild als 2D-float-Array.

    Returns
    -------
    img : np.ndarray (ny, nx), float64
    saturation_value : float
        Groesster darstellbarer Wert (255 bei 8 bit, 65535 bei 16 bit ...).
        Wird fuer die Uebersteuerungs-Warnung gebraucht.
    """
    with Image.open(path) as im:
        if im.mode in ("I;16", "I;16B", "I;16L", "I"):
            arr = np.asarray(im, dtype=np.float64)
            # 12-bit-Kameras speichern oft in 16-bit-Containern
            sat = 4095.0 if arr.max() <= 4095 else 65535.0
        elif im.mode == "F":
            arr = np.asarray(im, dtype=np.float64)
            sat = float(np.nanmax(arr))
        else:
            arr = np.asarray(im.convert("L"), dtype=np.float64)
            sat = 255.0
    return arr, sat


def list_images(folder: str | Path, skip_background: bool = True) -> list[Path]:
    folder = Path(folder)
    files = sorted(p for p in folder.iterdir() if p.is_file() and is_image_file(p))
    if skip_background:
        files = [p for p in files if not is_background_file(p)]
    return files
