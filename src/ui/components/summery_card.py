from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

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

        self.init_ui()

    def init_ui(self):

        # Main layout of SummaryCard
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Card background
        frame = QFrame()
        frame.setObjectName("summaryFrame")

        frame.setStyleSheet("""
            QFrame#summaryFrame {
                background-color: #d4d4d4;
                border-radius: 12px;
            }
        """)

        # Layout inside the card
        layout = QVBoxLayout(frame)
        layout.setObjectName("summaryLayout")

        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)

        # Title
        title_label = QLabel(self.title.capitalize())
        title_label.setObjectName("summaryTitle")

        title_color = COLOR_MAP.get(
            self.title.lower(),
            "#000000"
        )

        title_label.setStyleSheet(f"""
            QLabel#summaryTitle {{
                font-size: 16px;
                font-weight: bold;
                color: {title_color};
            }}
        """)

        # Value
        value_label = QLabel(str(self.value))
        value_label.setObjectName("summaryValue")

        value_label.setStyleSheet("""
            QLabel#summaryValue {
                font-size: 30px;
                color: #363535;
                font-weight: bold;
            }
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        # Add the frame to SummaryCard
        main_layout.addWidget(frame)