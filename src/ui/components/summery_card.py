from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from src.ui.styles.tokens import COLORS

COLOR_MAP = {
    "completed": "#4CAF50",
    "due soon": "#FF9800",
    "overdue": "#F44336",
}


class SummaryCard(QWidget):

    def __init__(self, title, value, parent=None):
        super().__init__(parent)

        self.title = title
        self.value = value

        self.setObjectName("summaryCard")

        self.init_ui()

        self.update_theme_styles()

    def init_ui(self):

        # Main layout of SummaryCard
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Card background
        self.frame = QFrame()
        self.frame.setObjectName("summaryFrame")

        # Layout inside the card
        layout = QVBoxLayout(self.frame)
        layout.setObjectName("summaryLayout")

        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)

        # Title
        self.title_label = QLabel(self.title.capitalize())
        self.title_label.setObjectName("summaryTitle")

        # Value
        self.value_label = QLabel(str(self.value))
        self.value_label.setObjectName("summaryValue")

        

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

        # Add the frame to SummaryCard
        main_layout.addWidget(self.frame)

    def update_theme_styles(self):

        try:
            title_text_color = COLOR_MAP[self.title]
        except ValueError:
            title_text_color = COLORS.text_secondary.name()

        self.frame.setStyleSheet(f"""
            QFrame#summaryFrame {{
                background-color: {COLORS.card_bg.name()};
                border-radius: 12px;
            }}

            QLabel#summaryValue {{
                font-size: 30px;
                color: {COLORS.text_secondary.name()};
                font-weight: bold;
            }}

            QLabel#summaryTitle {{
                font-size: 16px;
                font-weight: bold;
                color: {title_text_color};
            }}

        """)
