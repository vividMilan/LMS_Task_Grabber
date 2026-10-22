from zoneinfo import ZoneInfo
from PyQt6.QtCore import QSettings

APP_TIMEZONE = ZoneInfo("Asia/Colombo")

DUE_SOON = 7

def get_due_soon_days() -> int:
    """Returns the saved due soon days"""

    settings = QSettings("LMS Tracker", "LMS Tracker")

    return settings.value(
        "deadlines/due_soon_days",
        DUE_SOON,
        type=int
    )

def set_due_soon_days(days: int) -> None:
    """set due soon days"""

    if not 1 <= days <=30:
        raise ValueError("Due soon period must be between 1 - 30 days")

    settings = QSettings("LMS Tracker", "LMS Tracker")

    settings.setValue("deadlines/due_soon_days", days)