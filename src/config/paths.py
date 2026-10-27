import sys
from pathlib import Path


def get_app_dir() -> Path:
    """Return the folder containing the executable or project."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    # Project root: src/config/paths.py -> project root
    return Path(__file__).resolve().parents[2]


def get_data_dir() -> Path:
    """Return the application's data folder."""
    data_dir = get_app_dir() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_database_path() -> Path:
    return get_data_dir() / "assignments.db"