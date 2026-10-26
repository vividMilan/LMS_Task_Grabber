from datetime import datetime, timedelta

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.config.time import APP_TIMEZONE, get_due_soon_days
from src.database.connection import SessionLocal
from src.database.models import Assignment
from src.database.repositories.assignment_repository import assignment_repo
from src.domain.types.assignment import AssignmentData
from src.services.task_service import TaskService
from src.ui.components.summery_card import SummaryCard
from src.ui.components.task_card import TaskCard
from src.ui.styles.tokens import COLORS


class DashboardView(QWidget):

    assignment_updated = pyqtSignal()
    completed_changed = pyqtSignal(str, bool)


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
        today = datetime.now(APP_TIMEZONE).strftime("%A, %B %d, %Y")
        self.date_label = QLabel(f"{today}")

        heading_layout.setSpacing(4)

        heading_layout.addWidget(self.label)
        heading_layout.addWidget(self.date_label)


        # Task Summary Section
        self.summary_layout = QHBoxLayout()
        self.summary_layout.setObjectName("summaryLayout")

        # Upcoming Tasks Section
        self.upcoming_tasks_label = QLabel("Upcoming Tasks")
        
        self.upcoming_tasks_layout = QVBoxLayout()
        self.upcoming_tasks_layout.setSpacing(12)

        
        layout.addLayout(heading_layout)
        layout.addLayout(self.summary_layout)
        layout.addWidget(self.create_progress_bar())
        layout.addWidget(self.upcoming_tasks_label)
        layout.addLayout(self.upcoming_tasks_layout)

        self.refresh_dashboard()

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


    def create_progress_bar(self):

        self.progress_frame = QFrame()
        self.progress_frame.setObjectName("progressFrame")

        self.progress_title = QLabel("Overall Progression")
        self.progress_title.setObjectName("progressTitle")

        self.progress_label = QLabel("5%")
        self.progress_label.setObjectName("progressValue")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(20)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)

        self.progress_frame.setStyleSheet(f"""

            QFrame#progressFrame {{
                background-color: {COLORS.card_bg.name()};
                border-radius: 12px;
            }}

            QLabel#progressTitle {{
                font-size: 16px;
                font-weight: bold;
                color: {COLORS.text_primary.name()};
            }}

            QLabel#progressValue {{
                font-size: 30px;
                color: {COLORS.accent.name()};
                font-weight: bold;
            }}

            QProgressBar {{
                background-color: {COLORS.dark_bg.name()};
                border: none;
                border-radius: 5px;
            }}

            QProgressBar::chunk {{
                background-color: {COLORS.accent.name()};
                border-radius: 5px;
            }}
        """)

        self.progress_layout = QVBoxLayout(self.progress_frame)
        self.progress_layout.addWidget(self.progress_title)
        self.progress_layout.addWidget(self.progress_label)
        self.progress_layout.addWidget(self.progress_bar)

        return self.progress_frame

    def refresh_progress(self):

        db = SessionLocal()

        try:
            total = db.query(Assignment).count()

            completed = db.query(Assignment).filter(
                Assignment.completed.is_(True)
            ).count()

            percentage = round(
                completed/total * 100
            ) if total > 0 else 0

            self.progress_label.setText(f"{percentage}%")

            self.progress_bar.setValue(int(percentage))



        except SQLAlchemyError as e:
            print(f"Problem while refreshing progress: {e}")

        finally:
            db.close()

    def update_assignment_completion(self, task_id: str, is_completed: bool):
        try:
            updated = TaskService.set_completed(
                task_id=task_id,
                is_completed=is_completed
            )

            if updated:
                self.assignment_updated.emit()

        except SQLAlchemyError as exc:
            print(f"Error updating task completion: {exc}")

    def add_summary_cards(self):

        db = SessionLocal()

        completed_count = len(assignment_repo.get_upcoming(db))
        due_soon_count = len(assignment_repo.get_due_soon(db))
        overdue_count = len(assignment_repo.get_overdue(db))

        db.close()

        # Completed Tasks
        completedTasks = SummaryCard("pending", completed_count)
        dueSoonTasks = SummaryCard("due soon", due_soon_count)
        overdueTasks = SummaryCard("overdue", overdue_count)
        
        self.summary_layout.addWidget(completedTasks)
        self.summary_layout.addWidget(dueSoonTasks)
        self.summary_layout.addWidget(overdueTasks)

    

    def refresh_summary_card(self):

        while self.summary_layout.count():
            item = self.summary_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        db = SessionLocal()

        try:
            pending_count = (
                db.query(Assignment).filter(Assignment.completed.is_(False)).count()
            )

            due_soon_count = len(
                assignment_repo.get_due_soon(db)
            )

            overdue_count = len(
                assignment_repo.get_overdue(db)
            )
        finally:
            db.close()

        # Create the updated cards.

        completed_card = SummaryCard(
            "pending",
            pending_count
        )

        due_soon_card = SummaryCard(
            "due soon",
            due_soon_count
        )

        overdue_card = SummaryCard(
            "overdue",
            overdue_count
        )

        self.summary_layout.addWidget(completed_card)
        self.summary_layout.addWidget(due_soon_card)
        self.summary_layout.addWidget(overdue_card)

    def refresh_upcoming_tasks(self):
        while self.upcoming_tasks_layout.count():
            item = self.upcoming_tasks_layout.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        for assignment in self._get_upcoming_tasks():
            task_card = TaskCard(
                id=assignment.id,
                is_completed=assignment.completed,
                due=assignment.due,
                assignment_type=assignment.type,
                course_code=assignment.course_id,
                course_name=(
                    assignment.course.name if assignment.course else ""
                ),
                title=assignment.name
            )
            

            task_card.completed_changed.connect(
                self.completed_changed.emit
            )

            self.upcoming_tasks_layout.addWidget(task_card)


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

    def refresh_dashboard(self):
        self.refresh_summary_card()
        self.refresh_upcoming_tasks()
        self.refresh_progress()