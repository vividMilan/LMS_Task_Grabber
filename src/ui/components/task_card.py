from datetime import datetime

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.domain.enums.chip_types import ChipType
from src.ui.components.assignment_type_badge import assignmentType
from src.ui.components.detail_chip import DetailChip
from src.ui.styles.shadow_factory import apply_drop_shadow
from src.ui.styles.tokens import COLORS
from src.utils.strip_datetime import strip_due


class TaskCard(QWidget):

    clicked = pyqtSignal(object)
    completed_changed = pyqtSignal(str, bool)

    def __init__(
            self,
            id: str,
            title: str,
            course_code: str,
            due: datetime | None,
            assignment_type: str,
            course_name: str,
            is_completed: bool = False,
            parent=None,
    ):
        super().__init__(parent)

        self.id = id
        self.title = title
        self.course_code = course_code
        self.assignment_type = assignment_type
        self.course_name = course_name
        self.due = due
        self.is_completed = is_completed

        self.setObjectName("taskCard")

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        apply_drop_shadow(self, blur_radius=10, y_offset=4, x_offset=4, opacity=10)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._init_ui(
            id=id,
            title=title,
            course_code=course_code,
            assignment_type=assignment_type,
            course_name=course_name,
            due=due
        )

        self.update_theme_styles()

    def _init_ui(
            self,
            id: str,
            title: str,
            course_code: str,
            due: datetime,
            assignment_type: str,
            course_name: str = ""
    ):
        task_layout = QVBoxLayout(self)
        task_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        task_layout.setContentsMargins(20, 18, 20, 18)
        task_layout.setSpacing(12)


        heading_layout = QHBoxLayout()
        heading_layout.setContentsMargins(0, 0, 0, 0)
        heading_layout.setSpacing(8)

        self.checkbox = QCheckBox()
        self.checkbox.setObjectName("taskCheckBox")
        self.checkbox.setChecked(self.is_completed)
        self.checkbox.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.checkbox.toggled.connect(
            self._on_checkbox_toggled
        )

        heading_layout.addWidget(self.checkbox)
        
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
            footer_layout.addWidget(DetailChip("course", course_code, course_name))

        due_date = ""
        due_time = ""

        if due:
            due_date, due_time = strip_due(due=due)

        if due_date:
            footer_layout.addWidget(
                DetailChip(ChipType.DATE, due_date)
            )

        if (due_time):
            footer_layout.addWidget(
                DetailChip(ChipType.TIME, due_time)
            )

        footer_layout.addStretch() 

        task_layout.addLayout(heading_layout)
        task_layout.addLayout(footer_layout)

    def _on_checkbox_toggled(self, checked: bool) -> None:
        self.is_completed = checked
        self.update_theme_styles()
        self.completed_changed.emit(self.id, checked)

    def update_theme_styles(self):

        heading_color = COLORS.text_secondary.name() if self.is_completed else COLORS.text_primary.name()
        font_style = "text-decoration: line-through;" if self.is_completed else "text-decoration: none;"
        card_opacity = "0.5" if self.is_completed else "1.0"

        self.setStyleSheet(f"""
            QWidget#taskCard {{
                background-color: {COLORS.card_bg.name()};
                border: 1px solid {COLORS.border.name()};
                border-radius: 8px;
                padding: 16px;
                opacity: {card_opacity};
            }}

            QWidget#taskCard:hover {{
                border-color: {COLORS.accent.name()};
            }}

            QWidget#taskCard QLabel#headingLabel {{
                color: {heading_color};
                font-size: 16px;
                font-weight: bold;
                {font_style}
            }}

            QCheckBox#taskCheckBox {{
                spacing: 0px;
            }}

            QCheckBox#taskCheckBox::indicator {{
                width: 18px; 
                height: 18px;
                border: 2px solid {COLORS.border.name()};
                border-radius: 5px;
                background-color: transparent;
            }}

            QCheckBox#taskCheckBox::indicator:hover {{
                border-color: {COLORS.accent.name()};
            }}

            QCheckBox#taskCheckBox::indicator:checked {{
                background-color: {COLORS.accent.name()};
                border-color: {COLORS.border.name()};
                image: none;
            }}

            QCheckBox#taskCheckbox::indicator:checked {{
                border: 2px solid {COLORS.accent.name()};
                background-color: {COLORS.accent.name()};
            }}

        """)

        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.id)

        super().mousePressEvent(event)