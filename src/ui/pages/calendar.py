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

from datetime import datetime


class CalendarPage(QWidget):
    def __init__(self):
        super().__init__()

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

        self.calendar = QCalendarWidget()
        self.calendar.setFont(Theme.get_font(Theme.Fonts.SMALL))
        self.calendar.setGridVisible(False)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.HorizontalHeaderFormat.ShortDayNames)
        self.calendar.setSelectionMode(QCalendarWidget.SelectionMode.SingleSelection)
        self.calendar.setStyleSheet(f"""
            QCalendarWidget {{
                background-color: {Theme.Colors.BG_WHITE};
                border: none;
            }}

            QCalendarWidget QToolButton {{
                color: {Theme.Colors.TEXT_DARK};
                background: transparent;
                border: none;
                font-size: 14px;
                font-weight: 600;
                padding: 6px;
            }}

            QCalendarWidget QToolButton:hover {{
                color: {Theme.Colors.PRIMARY};
                background-color: {Theme.Colors.PAGE_BG};
                border-radius: 8px;
            }}

            QCalendarWidget QMenu {{
                background-color: white;
                color: {Theme.Colors.TEXT_DARK};
                border: 1px solid #ddd;
            }}

            QCalendarWidget QSpinBox {{
                color: {Theme.Colors.TEXT_DARK};
                background: transparent;
                border: none;
            }}

            QCalendarWidget QAbstractItemView:enabled {{
                background-color: {Theme.Colors.BG_WHITE};
                color: {Theme.Colors.TEXT_DARK};
                selection-background-color: {Theme.Colors.PRIMARY};
                selection-color: white;
            }}
        """)
        self.calendar.selectionChanged.connect(self._update_date_header)

        panel_layout.addWidget(self._build_month_header())
        panel_layout.addWidget(self.calendar)
        
        return panel

    def _build_month_header(self):

        date = self.calendar.selectedDate()

        month = date.toString("MMMM")
        year = date.year()

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        self.title = QLabel(month)
        self.title.setFont(Theme.get_font(Theme.Fonts.MEDIUM, bold=True))
        self.title.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")

        self.year = QLabel(str(year))
        self.year.setFont(Theme.get_font(Theme.Fonts.LARGE, bold=True))
        self.year.setStyleSheet(f"color: {Theme.Colors.PRIMARY};")

        header_layout.addWidget(self.title)
        header_layout.addWidget(self.year)
        header_layout.addStretch()
        return header
    
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

        date = QFrame()

        self.date_layout = QVBoxLayout(date)
        self.date_layout.setSpacing(0)

        self.date_title = QLabel("26th")
        self.date_title.setFont(Theme.get_font(Theme.Fonts.XLARGE, bold=True))
        self.date_title.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")

        self.date_subtitle = QLabel("Thursday")
        self.date_subtitle.setFont(Theme.get_font(Theme.Fonts.NORMAL))
        self.date_subtitle.setStyleSheet(f"color: {Theme.Colors.TEXT_MUTED};")

        self.date_layout.addWidget(self.date_title)
        self.date_layout.addWidget(self.date_subtitle)

        panel_layout.addWidget(date)

        panel_layout.addStretch()

        return panel

    def _update_date_header(self):
        date = self.calendar.selectedDate()
        day = date.day()
        suffix = "th" if 10 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        self.date_title.setText(f"{day}{suffix}")
        self.date_subtitle.setText(date.toString("dddd"))
        self.title.setText(date.toString("MMMM"))
        self.year.setText(str(date.year()))