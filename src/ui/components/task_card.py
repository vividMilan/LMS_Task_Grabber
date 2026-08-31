from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from typing import Optional
from PyQt6.QtCore import Qt

import qtawesome as qta

from src.ui.components.assignment_type_badge import assignmentType

from src.ui.components.detail_chip import DetailChip

class TaskCard(QWidget):
    def __init__(
            self, 
            title: str,
            course_code: str,
            due_date: str,
            due_time: str,
            assignment_type: str,
            file_count: Optional[int] = None,
            parent=None
        ):
        super().__init__(parent)
        self.setObjectName("taskCard")

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self._init_ui(
            title,
            course_code=course_code,
            due_date=due_date,
            due_time=due_time,
            file_count=file_count,
            assignment_type=assignment_type,
        )

    def _init_ui(
            self, 
            title: str,
            course_code: str,
            due_date: str,
            due_time: str,
            assignment_type: str,
            file_count: Optional[int] = None,
    ):
        task_layout = QVBoxLayout(self)
        task_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        task_layout.setContentsMargins(20, 18, 20, 18)
        task_layout.setSpacing(12)


        heading_layout = QHBoxLayout()
        heading_layout.setContentsMargins(0, 0, 0, 0)
        heading_layout.setSpacing(8)

        if assignment_type:
            assigment_type = assignmentType(assignment_type)
            heading_layout.addWidget(assigment_type)


        lbl_heading = QLabel(title)
        lbl_heading.setObjectName("headingLabel")

        heading_layout.addWidget(lbl_heading)
        heading_layout.addStretch()

        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(6)

        if course_code:
            footer_layout.addWidget(DetailChip("course", course_code))
        if due_date:
            footer_layout.addWidget(DetailChip("date", due_date))
        if due_time:
            footer_layout.addWidget(DetailChip("time", due_time))
        if file_count:
            footer_layout.addWidget(DetailChip("file", f"{file_count} files"))

        footer_layout.addStretch() 

        task_layout.addLayout(heading_layout)
        task_layout.addLayout(footer_layout)