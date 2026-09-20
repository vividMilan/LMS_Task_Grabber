from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCalendarWidget,
    QFrame,
    QHBoxLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.ui.components.task_card import TaskCard
from src.ui.styles.tokens import COLORS


class CalendarView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._init_ui()
        self.update_theme_styles()

    def _init_ui(self):
        layout = QHBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("assignmentScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()

        calender_layout = QVBoxLayout()
        assignment_layout = QVBoxLayout(self.scroll_content)
        assignment_layout.setContentsMargins(16, 16, 16, 16)
        assignment_layout.setSpacing(8)

        calendar = QCalendarWidget()

        # Add task cards
        for _ in range(10):
            assignment_layout.addWidget(
                TaskCard(
                    title="Database Management – TMA 01",
                    due_date="2026/08/12",
                    due_time="11:59PM",
                    course_code="EEX5432",
                    assignment_type="quiz",
                )
            )

        calender_layout.addWidget(calendar)
        calender_layout.addStretch()

        assignment_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)

        layout.addLayout(calender_layout, 3)
        layout.addWidget(self.scroll_area, 7)

    def update_theme_styles(self):

        self.scroll_area.setStyleSheet(f"""
            #assignmentScrollArea {{
                background-color: transparent;
                border: none;
            }}

            #assignmentScrollArea > QWidget > QWidget {{
                background-color: transparent;
            }}

            #assignmentScrollArea QScrollBar:vertical {{
                background-color: transparent;
                width: 8px;
                margin: 4px 0 4px 0;
            }}

            #assignmentScrollArea QScrollBar::handle:vertical {{
                background-color: {COLORS.border.name()};
                border-radius: 4px;
                min-height: 40px;
            }}

            #assignmentScrollArea QScrollBar::handle:vertical:hover {{
                background-color: {COLORS.text_secondary.name()};
            }}

            #assignmentScrollArea QScrollBar::add-line:vertical,
            #assignmentScrollArea QScrollBar::sub-line:vertical {{
                height: 0px;
            }}

            #assignmentScrollArea QScrollBar::add-page:vertical,
            #assignmentScrollArea QScrollBar::sub-page:vertical {{
                background: transparent;
            }}
        """)