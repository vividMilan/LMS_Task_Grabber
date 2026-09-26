from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QCalendarWidget,
    QFrame,
    QHBoxLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.database.connection import SessionLocal
from src.database.repositories.assignment_repository import assignment_repo
from src.ui.components.task_card import TaskCard
from src.ui.styles.tokens import COLORS, FONT_SIZES


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

        # ---------------- Calendar -------------------
        calendar_container = QFrame()

        today = QDate.currentDate()


        self.calendar = QCalendarWidget(calendar_container)
        self.calendar.setObjectName("calendar")
        
        # Show only one month
        self.calendar.setVerticalHeaderFormat(
            QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader
        )

        self.calendar.setGridVisible(False)

        self.calendar.setCurrentPage(
            today.year(),
            today.month()
        )

        self.calendar.setSelectedDate(today)

        self.calendar.selectionChanged.connect(self.date_selected)

        calender_layout = QVBoxLayout()
        self.assignment_layout = QVBoxLayout(self.scroll_content)
        self.assignment_layout.setContentsMargins(16, 16, 16, 16)
        self.assignment_layout.setSpacing(8)


        

        calender_layout.addWidget(self.calendar)
        calender_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)

        layout.addLayout(calender_layout, 3)
        layout.addWidget(self.scroll_area, 7)

    
    def date_selected(self):
        selected_date = self.calendar.selectedDate()
        python_date = selected_date.toPyDate()

        db = SessionLocal()

        try:
            assignments = assignment_repo.get_by_date(
                db=db,
                selected_date=python_date
            )

            self.render_assignments(assignments)

        finally:
            db.close()

    def clear_assignments(self):
        while self.assignment_layout.count():

            item = self.assignment_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def render_assignments(self, assignments):

        self.clear_assignments()

        # Add task cards
        for assignment in assignments:

            self.assignment_layout.addWidget(
                TaskCard(
                    title=assignment.name,
                    due_date=assignment.due.strftime("%Y/%m/%d"),
                    due_time=assignment.due.strftime("%I:%M %p"),
                    course_code=assignment.course_id,
                    assignment_type=assignment.type,
                )
            )

        self.assignment_layout.addStretch()
    
    def update_theme_styles(self):

        self.setStyleSheet(f"""

            #calendar QHeaderView {{
                background-color: transparent; 
            }}

            #calendar QHeaderView::section {{
                background-color: {COLORS.accent.name()};
                color: {COLORS.text_secondary.name()};
                border: none;
                padding: 4px;
                font-weight: bold;
                font-size: {FONT_SIZES.xs}px;
            }}

            #calendar QAbstractItemView {{
                background-color: {COLORS.dark_bg.name()};
                border-radius: 44px;
                color: {COLORS.text_primary.name()};
                selection-background-color: {COLORS.accent.name()};
                selection-color: #ffffff;
                border: none;
                outline: none;
                font-size: {FONT_SIZES.sm}px;
            }}

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