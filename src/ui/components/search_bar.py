import qtawesome as qta
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QWidget

from src.ui.styles.tokens import COLORS


class SearchBar(QWidget):
    def __init__(self, placeholder: str = "Search...", parent=None):
        super().__init__(parent)
        self.setObjectName("searchBarWidget")
        self._init_ui(placeholder)


    def _init_ui(self, placeholder: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.search_input = QLineEdit()
        self.search_input.setContentsMargins(0, 0, 0, 0)
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.setClearButtonEnabled(True)

        # Add magnifying glass icon on the left on QLine
        search_icon = qta.icon("mdi.magnify", color="#94A3B8")
        self.search_input.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)

        self.setStyleSheet("border-radius: 16px;")

        layout.addWidget(self.search_input)

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet(f"""

            #searchBarWidget #searchInput {{
                border-radius: 20px;
                padding: 12px 0px;
                height: 16px;
                color: {COLORS.window_bg.name()};
            }}

            #searchBarWidget #searchInput:focus {{
                border: 1.68px solid {COLORS.accent.name()};
            }}


        """)