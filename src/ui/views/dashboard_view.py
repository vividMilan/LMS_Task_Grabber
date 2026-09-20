from datetime import datetime
from zoneinfo import ZoneInfo

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.ui.components.summery_card import SummaryCard
from src.ui.styles.tokens import COLORS

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
        self.upcoming_tasks_label = QLabel("Upcoming Tasks")
        
        upcoming_tasks_layout.addWidget(self.upcoming_tasks_label)


        layout.addLayout(heading_layout)
        layout.addLayout(summary_layout)
        layout.addLayout(upcoming_tasks_layout)
        layout.addStretch()

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