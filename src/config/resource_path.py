# src/config/resource_path.py

import sys
from pathlib import Path


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False):
        # PyInstaller's bundled resource directory
        base_path = Path(sys._MEIPASS)
    else:
        # Project root: src/config/resource_path.py -> project root
        base_path = Path(__file__).resolve().parents[2]

    return base_path / relative_path