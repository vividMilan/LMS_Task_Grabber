from PyQt6.QtWidgets import QCalendarWidget, QHBoxLayout, QVBoxLayout, QWidget, QScrollArea, QFrame
from PyQt6.QtCore import Qt

from src.ui.components.task_card import TaskCard


class CalendarView(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()


        calender_layout = QVBoxLayout()
        assignment_layout = QVBoxLayout(scroll_content)
        assignment_layout.setContentsMargins(16, 16, 16, 16)
        assignment_layout.setSpacing(8)

        calendar = QCalendarWidget()
        assignment = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        assignment2 = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        assignment3 = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        assignment4 = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        assignment5 = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        assignment6 = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        assignment7 = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        assignment8 = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        assignment9 = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        assignment10 = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        calender_layout.addWidget(calendar)
        calender_layout.addStretch()

        assignment_layout.addWidget(assignment)
        assignment_layout.addWidget(assignment2)
        assignment_layout.addWidget(assignment3)
        assignment_layout.addWidget(assignment4)
        assignment_layout.addWidget(assignment5)
        assignment_layout.addWidget(assignment6)
        assignment_layout.addWidget(assignment7)
        assignment_layout.addWidget(assignment8)
        assignment_layout.addWidget(assignment9)
        assignment_layout.addWidget(assignment10)

        assignment_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        

        layout.addLayout(calender_layout, 3)
        layout.addWidget(scroll_area, 7)