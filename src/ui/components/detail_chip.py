from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame, QVBoxLayout
import qtawesome as qta

class DetailChip(QWidget):
    def __init__(self, content_type: str, content_str: str, parent=None):
        super().__init__(parent)
        self._init_ui(content_type=content_type, content_str=content_str)

    def _init_ui(self, content_type, content_str):
        # Main layout for the DetailChip widget
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        chip = QFrame()
        chip.setObjectName("chip")

        chip_layout = QHBoxLayout(chip)
        chip_layout.setContentsMargins(8, 4, 8, 4)
        chip_layout.setSpacing(4)

        if content_type == "course":
            icon = qta.icon("mdi6.book", color="#ffffff")
        elif content_type == "date":
            icon = qta.icon("fa5s.calendar-alt", color="#ffffff")
        elif content_type == "time":
            icon = qta.icon("mdi.clock-time-four", color="#ffffff")
        elif content_type == "file":
            icon = qta.icon("ei.paper-clip", color="#ffffff")

        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(14, 14))

        content_text = QLabel(content_str)

        chip_layout.addWidget(icon_label)
        chip_layout.addWidget(content_text)

        # Attach the frame to the widget's layout
        main_layout.addWidget(chip)