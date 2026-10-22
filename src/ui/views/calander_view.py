
from PyQt6.QtCore import QDate, QPointF, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import (
    QCalendarWidget,
    QFrame,
    QHBoxLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QLabel
)
from sqlalchemy.exc import SQLAlchemyError

from src.config.time import APP_TIMEZONE
from src.database.connection import SessionLocal
from src.database.models import Assignment
from src.database.repositories.assignment_repository import assignment_repo
from src.domain.types.assignment import AssignmentData
from src.ui.components.task_card import TaskCard
from src.ui.styles.tokens import COLORS, FONT_SIZES


class AssignmentCalendar(QCalendarWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.assignment_dates = set()
        self.indicator_color = QColor("#f39c12")

    def paintCell(self, painter, rect, date):
        # Draw the normal calendar cell first 

        super().paintCell(painter, rect, date)

        # Draw a dot if an assignment is due on this date
        if date.toPyDate() in self.assignment_dates:
            painter.save()
            painter.setRenderHint(
                QPainter.RenderHint.Antialiasing
            )
            painter.setPen(QPen(Qt.PenStyle.NoPen))

            painter.setBrush(QBrush(self.indicator_color))

            dot_radius = 3

            dot_x = rect.center().x()
            dot_y = rect.bottom() - 6

            painter.drawEllipse(
                QPointF(dot_x, dot_y),
                dot_radius,
                dot_radius
            )

            painter.restore()




class CalendarView(QWidget):

    assignment_clicked = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._init_ui()
        self.update_theme_styles()

        self.refresh_deadline_indicators()

        self.refresh_deadline_indicators()
        self.refresh_calendar()

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


        self.calendar = AssignmentCalendar(calendar_container)
        self.calendar = AssignmentCalendar(calendar_container)
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

        self.calendar.currentPageChanged.connect(
            self.refresh_deadline_indicators
        )

        self.calendar.currentPageChanged.connect(
            self.refresh_deadline_indicators
        )

        calender_layout = QVBoxLayout()
        self.assignment_layout = QVBoxLayout(self.scroll_content)
        self.assignment_layout.setContentsMargins(16, 16, 16, 16)
        self.assignment_layout.setSpacing(8)

        calender_layout.addWidget(self.calendar)
        calender_layout.addWidget(self.create_calendar_legend())
        calender_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)

        layout.addLayout(calender_layout, 3)
        layout.addWidget(self.scroll_area, 7)


    def refresh_deadline_indicators(self, year=None, month=None):
        """Highlight calendar dates based on assignment deadlines"""

        assignment_dates = set()

        with SessionLocal() as db:
            assignments = db.query(Assignment).all()

            for assignment in assignments:

                if not assignment.due:
                    continue

                due = assignment.due

                if due.tzinfo is None:
                    due = due.replace(tzinfo=APP_TIMEZONE)
                else:
                    due = due.astimezone(APP_TIMEZONE)

                if (
                    due.year == self.calendar.yearShown()
                    or due.month == self.calendar.monthShown()
                ):
                    assignment_dates.add(due.date())

            self.calendar.assignment_dates = assignment_dates
            self.calendar.updateCells()

    
    def date_selected(self):
        """Reload assignment when the user selects a date"""
        self.refresh_calendar()

    def clear_assignments(self):
        while self.assignment_layout.count():

            item = self.assignment_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def refresh_calendar(self):
        """Refresh assignments for the currently selected date."""
        selected_date = self.calendar.selectedDate()
        python_date = selected_date.toPyDate()

        db = SessionLocal()

        try:
            assignments = assignment_repo.get_by_date(
                db=db,
                selected_date=python_date
            )

            self.render_assignments(assignments=assignments)

        except SQLAlchemyError as exc:
            print(f"Failed to refresh calendar assignments: {exc}")
        finally:
            db.close()

    def render_assignments(self, assignments: list[AssignmentData]):

        self.clear_assignments()

        # Add task cards
        for assignment in assignments:

            task_card = TaskCard(
                id=assignment.id,
                title=assignment.name,
                due=assignment.due,
                course_code=assignment.course_id,
                assignment_type=assignment.type,
                course_name=assignment.course.name,
                is_completed=assignment.completed
            )

            task_card.clicked.connect(
                self.assignment_clicked.emit
            )

            self.assignment_layout.addWidget(
                task_card
            )

        self.assignment_layout.addStretch()

    def refresh_after_sync(self):
        """Refresh deadline indicator and assignments after syncing"""

        self.refresh_deadline_indicators()
        self.refresh_calendar()


    def create_calendar_legend(self):
        legend = QWidget()
        
        # Give the legend a sleek, modern card-like container background
        legend.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.02);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 8px;
            }
        """)
        
        layout = QHBoxLayout(legend)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(20)

        items = [
            (COLORS.accent.name(), "Assignment due"),
            (COLORS.success.name(), "Completed"),
            (COLORS.error.name(), "Overdue"),
        ]

        for color, text in items:
            item = QWidget()
            # Reset background/border for inner items so they inherit cleanly
            item.setStyleSheet("background: transparent; border: none;")
            
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(8)

            marker = QLabel()
            marker.setFixedSize(10, 10)
            # Modern circular dots instead of squares
            marker.setStyleSheet(
                f"background-color: {color};"
                "border-radius: 5px;"
            )

            label = QLabel(text)
            # Clean typography styling
            label.setStyleSheet(
                f"color: {COLORS.text_primary.name()};"
                "font-size: 12px;"
                "font-weight: 500;"
            )

            item_layout.addWidget(marker)
            item_layout.addWidget(label)

            layout.addWidget(item)

        layout.addStretch()

        return legend
    
    
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