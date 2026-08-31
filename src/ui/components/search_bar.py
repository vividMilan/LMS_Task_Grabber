from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget
from PyQt6.QtCore import Qt

import qtawesome as qta


class SearchBar(QWidget):
    def __init__(self, placeholder: str = "Search...", parent=None):
        super().__init__(parent)
        self.setObjectName("searchBarWidget")
        self._init_ui(placeholder)


    def _init_ui(self, placeholder: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        input = QLineEdit()
        input.setContentsMargins(0, 0, 0, 0)
        input.setObjectName("searchInput")
        input.setPlaceholderText(placeholder)
        input.setClearButtonEnabled(True)

        # Add magnifying glass icon on the left on QLine
        search_icon = qta.icon("mdi.magnify", color="#94A3B8")
        input.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)

        self.setStyleSheet("border-radius: 16px;")

        layout.addWidget(input)