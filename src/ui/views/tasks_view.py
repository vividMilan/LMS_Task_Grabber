
from datetime import datetime, timedelta

import qtawesome as qta
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from sqlalchemy.exc import SQLAlchemyError

from src.config.time import APP_TIMEZONE
from src.database.connection import SessionLocal
from src.database.models import Assignment
from src.domain.types.assignment import AssignmentData
from src.ui.components.search_bar import SearchBar
from src.ui.components.task_card import TaskCard
from src.ui.styles.tokens import COLORS


class TasksView(QWidget):

    assignment_clicked = pyqtSignal(object)
    sync_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("taskView")

        self._init_ui()
        self.update_theme_styles()
        self.load_assingments()

    # --------------------------------------------------
    # UI SETUP
    # --------------------------------------------------

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()

        self.title = QLabel("Upcoming Tasks")

        self.btn_sync = QPushButton("Sync Tasks")
        self.btn_sync.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.btn_sync.setObjectName("syncButton")
        self.btn_sync.setIcon(
            qta.icon("fa5s.sync-alt", color="#ffffff")
        )

        self.btn_sync.clicked.connect(
            self.sync_requested.emit
        )

        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_sync)

        # Search and filter row
        search_layout = QHBoxLayout()

        self.search_bar = SearchBar(
            placeholder="Search..."
        )

        self.search_bar.search_input.textChanged.connect(
            self.load_assingments
        )

        self.filter_combo = QComboBox()
        self.filter_type_combo = QComboBox()

        self.filter_combo.addItem(
            "Pending", "pending"
        )
        self.filter_combo.addItem(
            "Completed", "completed"
        )
        self.filter_combo.addItem(
            "All Tasks", "all"
        )
        self.filter_combo.addItem(
            "Overdue", "overdue"
        )
        self.filter_combo.addItem(
            "Due Today", "today"
        )
        self.filter_combo.addItem(
            "Next 7 Days", "week"
        )


        # type combo Items

        self.filter_type_combo.addItem(
            "All", "all"
        )

        self.filter_type_combo.addItem(
            "Quiz", "quiz"
        )

        self.filter_type_combo.addItem(
            "Viva Slot", "viva_slot"
        )

        self.filter_type_combo.addItem(
            "TMA", "tma"
        )

        self.filter_type_combo.addItem(
            "Exam", "exam"
        )

        self.filter_type_combo.addItem(
            "Mini Project", "mini_project"
        )


        self.filter_combo.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.filter_type_combo.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.filter_combo.currentIndexChanged.connect(
            self.load_assingments
        )

        self.filter_type_combo.currentIndexChanged.connect(
            self.load_assingments
        )

        search_layout.addWidget(self.search_bar, 1)
        search_layout.addWidget(self.filter_combo)
        search_layout.addWidget(self.filter_type_combo)

        # Task cards
        self.tasks_layout = QVBoxLayout()
        self.tasks_layout.setSpacing(12)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(self.tasks_layout)
        main_layout.addStretch()


    # --------------------------------------------------
    # MATCH SEARCH QUERY
    # --------------------------------------------------
    def _matches_search(self, assignment: Assignment, query: str) -> bool:

        query = query.strip().casefold()

        if not query:
            return True

        assignment_name = assignment.name or ""
        course_code = assignment.course_id or ""

        course_name = (
            assignment.course.name
            if getattr(assignment, "course", None)
            else ""
        )

        searchable_text = " ".join([
            assignment_name,
            str(course_code),
            course_name
        ]).casefold()

        return query in searchable_text

    # --------------------------------------------------
    # THEME
    # --------------------------------------------------

    def update_theme_styles(self):
        self.title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {COLORS.text_primary.name()};
        """)

        self.setStyleSheet(f"""
            QComboBox {{
                color: {COLORS.text_primary.name()};
                background-color: {COLORS.card_bg.name()};
                border: 1px solid {COLORS.border.name()};
                border-radius: 6px;
                padding: 8px 12px;
                min-width: 130px;
            }}

            QComboBox:hover {{
                border-color: {COLORS.accent.name()};
            }}

            QComboBox QAbstractItemView {{
                color: {COLORS.text_primary.name()};
                background-color: {COLORS.card_bg.name()};
                selection-background-color: {COLORS.accent.name()};
            }}
        """)

    # --------------------------------------------------
    # SYNC BUTTON
    # --------------------------------------------------

    def set_syncing(self, syncing: bool):
        self.btn_sync.setDisabled(syncing)

        if syncing:
            self.btn_sync.setText("Syncing...")
        else:
            self.btn_sync.setText("Sync Tasks")

        self.btn_sync.setIcon(
            qta.icon("fa5s.sync-alt", color="#FFFFFF")
        )

    # --------------------------------------------------
    # DATE HANDLING
    # --------------------------------------------------

    @staticmethod
    def _normalise_due(due: datetime) -> datetime:
        """
        Convert a deadline to the application's timezone.

        Naive database datetimes are assumed to represent
        local time in APP_TIMEZONE.
        """
        if due is None:
            return None

        if due.tzinfo is None:
            return due.replace(tzinfo=APP_TIMEZONE)

        return due.astimezone(APP_TIMEZONE)

    # --------------------------------------------------
    # FILTERING
    # --------------------------------------------------

    def _matches_type_filter(
        self,
        assignment: AssignmentData,
        selected_filter
    ): 

        if selected_filter == "all":
            return True
        
        if selected_filter == assignment.type:
            return True

    def _matches_filter(
        self,
        assignment: AssignmentData,
        selected_filter,
        now: datetime,
    ):
        due = self._normalise_due(assignment.due)

        # Include every assignment.
        if selected_filter == "all":
            return True

        # Completed assignments have their own category.
        if selected_filter == "completed":
            return assignment.completed

        if selected_filter == "pending":
            return not assignment.completed

        # The remaining categories contain incomplete tasks.
        if assignment.completed:
            return False

        # A deadline earlier than now is overdue.
        if selected_filter == "overdue":
            return due is not None and due < now

        # Deadline is today and has not passed.
        if selected_filter == "today":
            return (
                due is not None
                and due.date() == now.date()
                and due >= now
            )

        # Deadline falls within the next seven days.
        if selected_filter == "week":
            end_of_window = now + timedelta(days=7)

            return (
                due is not None
                and now <= due <= end_of_window
            )

        return True

    # --------------------------------------------------
    # TASK CARD CREATION
    # --------------------------------------------------

    def create_task_card(self, assignment: AssignmentData):
        course_name = (
            assignment.course.name
            if getattr(assignment, "course", None)
            else ""
        )

        task_card = TaskCard(
            id=assignment.id,
            title=assignment.name,
            due=assignment.due,
            course_code=assignment.course_id,
            assignment_type=assignment.type,
            course_name=course_name,
            is_completed=assignment.completed
        )

        self.tasks_layout.addWidget(task_card)

        task_card.completed_changed.connect(
            self.update_assignment_completion
        )

        task_card.clicked.connect(
            self.assignment_clicked.emit
        )

    # --------------------------------------------------
    # REFRESH
    # --------------------------------------------------

    def refresh_tasks(self):
        self.load_assingments()

    # --------------------------------------------------
    # LOAD, FILTER, AND DISPLAY
    # --------------------------------------------------

    def load_assingments(self, *_):
        # Remove existing cards and empty-state messages.
        while self.tasks_layout.count():
            item = self.tasks_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        db = SessionLocal()

        try:
            # Retrieve all assignments, including overdue ones.
            assignments = db.query(Assignment).all()

            # Read the filter's internal value.
            selected_filter = (
                self.filter_combo.currentData()
            )

            selected_type_filter = (
                self.filter_type_combo.currentData()
            )

            # Use the application's configured timezone.
            now = datetime.now(APP_TIMEZONE)

            search_query = self.search_bar.search_input.text()

            # Keep only assignments matching the filter.
            filtered_assignments = [
                assignment
                for assignment in assignments
                if (
                    self._matches_filter(
                        assignment,
                        selected_filter,
                        now,
                    )
                    and self._matches_search(
                        assignment,
                        search_query
                    )
                    and self._matches_type_filter(
                        assignment,
                        selected_type_filter
                    )
                )
            ]

            # Sort by deadline, placing undated tasks last.
            def sort_key(assignment: AssignmentData):
                due = self._normalise_due(
                    assignment.due
                )

                if due is None:
                    return (1, datetime.max.replace(
                        tzinfo=APP_TIMEZONE
                    ))

                return (0, due)

            filtered_assignments.sort(key=sort_key)

            # Show an empty-state message when necessary.
            if not filtered_assignments:
                empty_label = QLabel(
                    "No assignments found for this filter."
                )

                empty_label.setAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                empty_label.setStyleSheet(f"""
                    color: {COLORS.text_secondary.name()};
                    padding: 24px;
                    font-size: 14px;
                """)

                self.tasks_layout.addWidget(empty_label)

            # Create cards while the database session is open.
            for assignment in filtered_assignments:
                self.create_task_card(assignment)

            print(
                f"Loaded {len(filtered_assignments)} "
                f"assignments using filter: "
                f"{selected_filter}"
                f"{selected_type_filter}"
            )

        except SQLAlchemyError as exc:
            print(
                f"Error loading assignments: {exc}"
            )

            error_label = QLabel(
                "Unable to load assignments. "
                "Check the application logs."
            )

            error_label.setWordWrap(True)
            error_label.setStyleSheet(
                f"color: {COLORS.text_secondary.name()};"
            )

            self.tasks_layout.addWidget(error_label)

        finally:
            db.close()

    def update_assignment_completion(self, task_id, is_completed):
        db = SessionLocal()

        try: 

            assignment = db.query(Assignment).filter(Assignment.id == task_id).first()

            if assignment:
                assignment.completed = is_completed
                db.commit()

                self.load_assingments()

        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error updating task completion: {e}")
        finally:
            db.close()