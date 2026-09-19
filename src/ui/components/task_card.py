from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.ui.components.assignment_type_badge import assignmentType
from src.ui.components.detail_chip import DetailChip
from src.ui.styles.shadow_factory import apply_drop_shadow
from src.ui.styles.tokens import COLORS


class TaskCard(QWidget):

    clicked = pyqtSignal(object)

    def __init__(
            self, 
            title: str,
            course_code: str,
            due_date: str,
            due_time: str,
            assignment_type: str,
            file_count: int | None = None,
            parent=None
        ):
        super().__init__(parent)

        self.title = title
        self.course_code = course_code
        self.due_date = due_date
        self.due_time = due_time
        self.assignment_type = assignment_type
        self.file_count = file_count

        self.setObjectName("taskCard")

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        apply_drop_shadow(self, blur_radius=10, y_offset=4, x_offset=4, opacity=10)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._init_ui(
            title,
            course_code=course_code,
            due_date=due_date,
            due_time=due_time,
            file_count=file_count,
            assignment_type=assignment_type,
        )

        self.update_theme_styles()

    def _init_ui(
            self, 
            title: str,
            course_code: str,
            due_date: str,
            due_time: str,
            assignment_type: str,
            file_count: int | None = None,
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

    def update_theme_styles(self):
        self.setStyleSheet(f"""
            QWidget#taskCard {{
                background-color: {COLORS.card_bg.name()};
                border: 1px solid {COLORS.border.name()};
                border-radius: 8px;
                padding: 16px;
            }}

            QWidget#taskCard:hover {{
                border-color: {COLORS.accent.name()};
            }}

            QWidget#taskCard QLabel#headingLabel {{
                color: {COLORS.text_primary.name()};
                font-size: 16px;
                font-weight: bold;
            }}

        """)

        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)

        super().mousePressEvent(event)