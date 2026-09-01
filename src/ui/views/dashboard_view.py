from datetime import datetime

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.ui.components.summery_card import SummaryCard


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(20)
        self.setLayout(layout)

        # Heading Section
        heading_layout = QHBoxLayout()
        label = QLabel("Welcome to the Dashboard! 👋")
        label.setStyleSheet("font-size: 24px; font-weight: bold;")


        # Date Section
        today = datetime.now().strftime("%A, %B %d, %Y")
        date_label = QLabel(f"{today}")
        date_label.setStyleSheet("font-size: 16px; color: gray; font-weight: bold;")

        heading_layout.addWidget(label)
        heading_layout.addStretch()
        heading_layout.addWidget(date_label)


        # Task Summary Section
        summary_layout = QHBoxLayout()
        summary_layout.setObjectName("summaryLayout")

        # Completed Tasks
        completedTasks = SummaryCard("completed", 10)
        dueSoonTasks = SummaryCard("due soon", 5)
        overdueTasks = SummaryCard("overdue", 2)

        summary_layout.addWidget(completedTasks)
        summary_layout.addWidget(dueSoonTasks)
        summary_layout.addWidget(overdueTasks)


        # Upcoming Tasks Section
        upcoming_tasks_layout = QVBoxLayout()
        upcoming_tasks_label = QLabel("Upcoming Tasks")
        upcoming_tasks_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        upcoming_tasks_layout.addWidget(upcoming_tasks_label)


        layout.addLayout(heading_layout)
        layout.addLayout(summary_layout)
        layout.addLayout(upcoming_tasks_layout)
        layout.addStretch()