from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from ui.theme import Theme
import qtawesome as qta

class TaskCard(QFrame):
    def __init__(self, task):
        super().__init__()
        self.setObjectName("taskCard")
        self.setStyleSheet(
            f"""
            QFrame#taskCard {{
                background-color: {Theme.Colors.CARD_BG};
                border-radius: 20px;
                padding: 18px 40px;
            }}
            """
        )

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(4)

        title = QLabel(task.name)
        title.setWordWrap(True)
        title.setFont(Theme.get_font(Theme.Fonts.MEDIUM, bold=True))
        title.setStyleSheet(
            f"""
            color: {Theme.Colors.TEXT_DARK};
            background-color: transparent;
            """
        )
        card_layout.addWidget(title)

        meta_row = QWidget()
        meta_row.setStyleSheet(f"""
            background-color: transparent;
        """)
        meta_layout = QHBoxLayout(meta_row)
        meta_layout.setContentsMargins(0, 0, 0, 0)
        meta_layout.setSpacing(10)

        meta_layout.addWidget(self._create_badge("fa5s.book", task.courseCode, task.course))
        meta_layout.addWidget(self._create_badge("fa5s.calendar-alt", task.due_date))
        meta_layout.addWidget(self._create_badge("fa5s.clock", task.due_time))
        meta_layout.addStretch()

        card_layout.addWidget(meta_row)

    def _create_badge(self, icon_name, text, tooltip=None):
        badge = QFrame()

        badge.setStyleSheet(
            f"""
            QFrame {{
                background-color: {Theme.Colors.BADGE_BG};
                border-radius: 24px;
                padding: 8px;
            }}
            QLabel {{
                color: {Theme.Colors.BADGE_TEXT};
            }}
            """
        )

        if tooltip:
            badge.setToolTip(tooltip)

        layout = QHBoxLayout(badge)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color=Theme.Colors.BADGE_TEXT).pixmap(16, 16))
        icon.setContentsMargins(0, 0, 0, 0)

        label = QLabel(text)
        label.setFont(Theme.get_font(Theme.Fonts.SMALL, bold=True))
        label.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(icon)
        layout.addWidget(label)


        return badge