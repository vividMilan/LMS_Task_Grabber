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
from .theme import Theme


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {Theme.Colors.PAGE_BG};")

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(24, 24, 24, 24)
        page_layout.setSpacing(20)

        page_layout.addWidget(self._build_search_bar())
        page_layout.addWidget(self._build_header())
        page_layout.addWidget(self._build_task_list())

    def _build_search_bar(self):
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by course code or date")
        search_input.setFixedHeight(44)
        search_input.setFont(Theme.get_font(Theme.Fonts.NORMAL))
        search_input.setStyleSheet(
            f"""
            QLineEdit {{
                border: none;
                border-radius: 22px;
                padding: 0 16px;
                background-color: {Theme.Colors.SEARCH_BG};
                color: {Theme.Colors.TEXT_DARK};
            }}
            QLineEdit:focus {{
                outline: none;
                border: 2px solid {Theme.Colors.PRIMARY};
            }}
            """
        )
        return search_input

    def _build_header(self):
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        label = QLabel("Upcoming Tasks")
        label.setFont(Theme.get_font(Theme.Fonts.XLARGE, bold=True))
        label.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")

        header_layout.addWidget(label)
        header_layout.addStretch()
        return header

    def _build_task_list(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)

        tasks = [
            {
                "title": "Student count for Final Presentation to be held at Rathnapura and Badulla Centre",
                "course": "EEX3249",
                "date": "2026/02/25",
                "time": "23:59",
            },
            {
                "title": "Student count for Final Presentation to be held at Rathnapura and Badulla Centre",
                "course": "EEX3249",
                "date": "2026/02/25",
                "time": "23:59",
            },
        ]

        for task in tasks:
            content_layout.addWidget(self._create_task_card(task))

        content_layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def _create_task_card(self, task):
        card = QFrame()
        card.setObjectName("taskCard")
        card.setStyleSheet(
            f"""
            QFrame#taskCard {{
                background-color: {Theme.Colors.CARD_BG};
                border-radius: 20px;
                padding: 18px;
            }}
            """
        )

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(14)

        title = QLabel(task["title"])
        title.setWordWrap(True)
        title.setFont(Theme.get_font(Theme.Fonts.MEDIUM, bold=True))
        title.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")
        card_layout.addWidget(title)

        meta_row = QWidget()
        meta_layout = QHBoxLayout(meta_row)
        meta_layout.setContentsMargins(0, 0, 0, 0)
        meta_layout.setSpacing(10)

        meta_layout.addWidget(self._create_badge("fa5s.book", task["course"]))
        meta_layout.addWidget(self._create_badge("fa5s.calendar-alt", task["date"]))
        meta_layout.addWidget(self._create_badge("fa5s.clock", task["time"]))
        meta_layout.addStretch()

        card_layout.addWidget(meta_row)
        return card

    def _create_badge(self, icon_name, text):
        badge = QFrame()
        badge.setStyleSheet(
            f"""
            QFrame {{
                background-color: {Theme.Colors.BADGE_BG};
                border-radius: 14px;
                padding: 8px 12px;
            }}
            QLabel {{
                color: {Theme.Colors.BADGE_TEXT};
            }}
            """
        )

        layout = QHBoxLayout(badge)
        layout.setContentsMargins(2, 1, 2, 1)
        layout.setSpacing(4)

        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color=Theme.Colors.BADGE_TEXT).pixmap(18, 18))
        icon.setFixedSize(18, 18)
        layout.addWidget(icon)

        label = QLabel(text)
        label.setFont(Theme.get_font(Theme.Fonts.SMALL, bold=True))
        layout.addWidget(label)

        return badge


class CalendarPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: {Theme.Colors.PAGE_BG};")

        content_layout = QHBoxLayout(self)
        content_layout.setContentsMargins(6, 6, 6, 6)
        content_layout.setSpacing(20)

        content_layout.addWidget(self._build_left_panel(), 0)
        content_layout.addWidget(self._build_right_panel(), 1)

    def _build_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet(
            f"""
            QFrame {{
                background-color: {Theme.Colors.BG_WHITE};
                border-radius: 24px;
            }}
            """
        )

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 24, 24, 24)
        panel_layout.setSpacing(20)

        panel_layout.addWidget(self._build_month_header())

        self.calendar = QCalendarWidget()
        self.calendar.setFont(Theme.get_font(Theme.Fonts.SMALL))
        self.calendar.setGridVisible(False)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.ShortDayNames)
        self.calendar.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
        self.calendar.setStyleSheet(
            f"""
            QCalendarWidget QWidget {{
                background-color: {Theme.Colors.BG_WHITE};
            }}
            QCalendarWidget QAbstractItemView:enabled {{
                background-color: {Theme.Colors.BG_WHITE};
                selection-background-color: {Theme.Colors.PRIMARY};
                selection-color: {Theme.Colors.BG_WHITE};
            }}
            QCalendarWidget QToolButton {{
                height: 32px;
                icon-size: 20px;
                font: bold 12px "{Theme.Fonts.FAMILY}";
            }}
            QCalendarWidget QSpinBox {{
                width: 100px;
                font: 12px "{Theme.Fonts.FAMILY}";
            }}
            """
        )
        self.calendar.selectionChanged.connect(self._update_date_header)

        panel_layout.addWidget(self.calendar)
        panel_layout.addWidget(self._build_activities_card())
        return panel

    def _build_month_header(self):
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        title = QLabel("February")
        title.setFont(Theme.get_font(Theme.Fonts.LARGE, bold=True))
        title.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")

        year = QLabel("2020")
        year.setFont(Theme.get_font(Theme.Fonts.MEDIUM, bold=True))
        year.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")

        header_layout.addWidget(title)
        header_layout.addWidget(year)
        header_layout.addStretch()
        return header

    def _build_activities_card(self):
        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {Theme.Colors.CARD_BG};
                border-radius: 18px;
                min-height: 120px;
            }}
            """
        )

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Activities")
        title.setFont(Theme.get_font(Theme.Fonts.MEDIUM, bold=True))
        title.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")
        layout.addWidget(title)

        placeholder = QLabel("")
        placeholder.setFixedHeight(40)
        placeholder.setStyleSheet(
            f"""
            QLabel {{
                background-color: {Theme.Colors.PAGE_BG};
                border-radius: 12px;
            }}
            """
        )
        layout.addWidget(placeholder)

        return card

    def _build_right_panel(self):
        panel = QFrame()
        panel.setStyleSheet(
            f"""
            QFrame {{
                background-color: {Theme.Colors.BG_WHITE};
                border-radius: 24px;
            }}
            """
        )

        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(24, 24, 24, 24)
        panel_layout.setSpacing(24)

        self.date_title = QLabel("26th")
        self.date_title.setFont(Theme.get_font(Theme.Fonts.XLARGE, bold=True))
        self.date_title.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")

        self.date_subtitle = QLabel("Thursday, 26 February")
        self.date_subtitle.setFont(Theme.get_font(Theme.Fonts.NORMAL))
        self.date_subtitle.setStyleSheet(f"color: {Theme.Colors.TEXT_MUTED};")

        panel_layout.addWidget(self.date_title)
        panel_layout.addWidget(self.date_subtitle)
        panel_layout.addWidget(self._create_task_card({
            "title": "Student count for Final Presentation to be held at Rathnapura and Badulla Centre",
            "course": "EEX3249",
            "date": "2026/02/25",
            "time": "23:59",
        }))
        panel_layout.addStretch()

        return panel

    def _update_date_header(self):
        date = self.calendar.selectedDate()
        day = date.day()
        suffix = "th" if 10 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        self.date_title.setText(f"{day}{suffix}")
        self.date_subtitle.setText(date.toString("dddd, d MMMM"))

    def _create_task_card(self, task):
        card = QFrame()
        card.setObjectName("taskCard")
        card.setStyleSheet(
            f"""
            QFrame#taskCard {{
                background-color: {Theme.Colors.CARD_BG};
                border-radius: 20px;
                padding: 18px;
            }}
            """
        )

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(14)

        title = QLabel(task["title"])
        title.setWordWrap(True)
        title.setFont(Theme.get_font(Theme.Fonts.MEDIUM, bold=True))
        title.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")
        card_layout.addWidget(title)

        meta_row = QWidget()
        meta_layout = QHBoxLayout(meta_row)
        meta_layout.setContentsMargins(0, 0, 0, 0)
        meta_layout.setSpacing(10)

        meta_layout.addWidget(self._create_badge("fa5s.book", task["course"]))
        meta_layout.addWidget(self._create_badge("fa5s.calendar-alt", task["date"]))
        meta_layout.addWidget(self._create_badge("fa5s.clock", task["time"]))
        meta_layout.addStretch()

        card_layout.addWidget(meta_row)
        return card

    def _create_badge(self, icon_name, text):
        badge = QFrame()
        badge.setStyleSheet(
            f"""
            QFrame {{
                background-color: {Theme.Colors.BADGE_BG};
                border-radius: 14px;
                padding: 8px 12px;
            }}
            QLabel {{
                color: {Theme.Colors.BADGE_TEXT};
            }}
            """
        )

        layout = QHBoxLayout(badge)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)

        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color=Theme.Colors.BADGE_TEXT).pixmap(14, 14))
        layout.addWidget(icon)

        label = QLabel(text)
        label.setFont(Theme.get_font(Theme.Fonts.SMALL, bold=True))
        layout.addWidget(label)

        return badge


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Settings Page")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(Theme.get_font(Theme.Fonts.LARGE, bold=True))
        layout.addWidget(label)