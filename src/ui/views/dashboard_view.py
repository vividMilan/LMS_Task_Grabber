from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.config.time import APP_TIMEZONE, get_due_soon_days
from src.database.connection import SessionLocal
from src.database.models import Assignment
from src.database.repositories.assignment_repository import assignment_repo
from src.ui.components.summery_card import SummaryCard
from src.ui.components.task_card import TaskCard
from src.ui.styles.tokens import COLORS

from src.domain.types.assignment import AssignmentData

from sqlalchemy.orm import joinedload

local_timezone = ZoneInfo("Asia/Colombo")

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("dashboardView")

        self._init_ui()

        self.update_theme_styles()


    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Heading Section
        heading_layout = QVBoxLayout()
        self.label = QLabel("Welcome to the Dashboard! 👋")

        # Date Section
        today = datetime.now(local_timezone).strftime("%A, %B %d, %Y")
        self.date_label = QLabel(f"{today}")

        heading_layout.setSpacing(4)

        heading_layout.addWidget(self.label)
        heading_layout.addWidget(self.date_label)


        # Task Summary Section
        self.summary_layout = QHBoxLayout()
        self.summary_layout.setObjectName("summaryLayout")

        self.add_summary_cards()

        # Upcoming Tasks Section
        upcoming_tasks_layout = QVBoxLayout()
        self.upcoming_tasks_label = QLabel("Upcoming Tasks")

        
        layout.addLayout(heading_layout)
        layout.addLayout(self.summary_layout)
        layout.addLayout(upcoming_tasks_layout)
        upcoming_tasks_layout.addWidget(self.upcoming_tasks_label)

        filtered_assignments = self._get_upcoming_tasks()

        for assignment in filtered_assignments:

            course_name = (
                assignment.course.name
                if getattr(assignment, "course", None)
                else ""
            )

            task_card = TaskCard(
                id=assignment.id,
                title=assignment.name,
                due=assignment.due,
                assignment_type=assignment.type,
                course_code=assignment.course_id,
                course_name=course_name,
                is_completed=assignment.completed,
            )

            upcoming_tasks_layout.addWidget(task_card)

        layout.addStretch()

    def _get_upcoming_tasks(self) -> list[AssignmentData]:
        due_soon_days = get_due_soon_days()
        now = datetime.now(APP_TIMEZONE)
        deadline = now + timedelta(days=due_soon_days)

        db = SessionLocal()

        filtered_assignments = []


        try:
            assignments = (
                db.query(Assignment).options(joinedload(Assignment.course)).all()
            )
            
            for assignment in assignments:

                due = assignment.due

                if assignment.completed:
                    continue

                if due.tzinfo is None:
                    due = due.replace(tzinfo=APP_TIMEZONE)
                else:
                    due = due.astimezone(APP_TIMEZONE)

                if now < due <= deadline:
                    filtered_assignments.append(assignment)

            filtered_assignments.sort(
                key=lambda assignment: assignment.due
            )

            return filtered_assignments

        finally:
            db.close()


    def add_summary_cards(self):

        db = SessionLocal()

        completed_count = len(assignment_repo.get_upcoming(db))
        due_soon_count = len(assignment_repo.get_due_soon(db))
        overdue_count = len(assignment_repo.get_overdue(db))

        db.close()

        # Completed Tasks
        completedTasks = SummaryCard("incomplete", completed_count)
        dueSoonTasks = SummaryCard("due soon", due_soon_count)
        overdueTasks = SummaryCard("overdue", overdue_count)
        
        self.summary_layout.addWidget(completedTasks)
        self.summary_layout.addWidget(dueSoonTasks)
        self.summary_layout.addWidget(overdueTasks)

    def update_theme_styles(self):
        self.label.setStyleSheet(f"""
            color: {COLORS.text_primary.name()};
            font-size: 24px; 
            font-weight: bold;
        """)
        self.date_label.setStyleSheet(f"""
            font-size: 16px; 
            color: {COLORS.text_secondary.name()}; 
            font-weight: bold;
        """)

        self.upcoming_tasks_label.setStyleSheet(f"""
            font-size: 20px; 
            font-weight: bold;
            color: {COLORS.text_primary.name()}
        """)