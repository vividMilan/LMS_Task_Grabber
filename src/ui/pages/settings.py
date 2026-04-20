from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QFrame,
    QHBoxLayout,
    QScrollArea,
    QCalendarWidget,
)
from PyQt6.QtCore import Qt
import qtawesome as qta
from ..theme import Theme


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Settings Page")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(Theme.get_font(Theme.Fonts.LARGE, bold=True))
        layout.addWidget(label)