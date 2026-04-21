from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel
import qtawesome as qta
from ui.theme import Theme

class Badge(QFrame):
    def __init__(self, icon_name, text, tooltip=None):
        super().__init__()

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {Theme.Colors.BADGE_BG};
                border-radius: 24px;
                padding: 8px 12px;
            }}
            QLabel {{
                color: {Theme.Colors.BADGE_TEXT};
            }}
            """
        )

        if tooltip:
            self.setToolTip(tooltip)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color=Theme.Colors.BADGE_TEXT).pixmap(16, 16))
        icon.setContentsMargins(0, 0, 0, 0)

        label = QLabel(text)
        label.setFont(Theme.get_font(Theme.Fonts.SMALL, bold=True))
        label.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(icon)
        layout.addWidget(label)
