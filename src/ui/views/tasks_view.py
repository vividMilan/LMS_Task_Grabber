import qtawesome as qta
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.ui.components.search_bar import SearchBar
from src.ui.components.task_card import TaskCard
from src.ui.styles.tokens import COLORS


class TasksView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("taskView")

        self._init_ui()

        self.update_theme_styles()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        header_layout = QHBoxLayout()
        self.title = QLabel("Upcoming Tasks")

        btn_sync = QPushButton("Sync Tasks")
        btn_sync.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sync.setObjectName("syncButton")
        btn_sync.setIcon(qta.icon("fa5s.sync-alt", color="#ffffff"))

        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header_layout.addWidget(btn_sync)

        search_layout = QHBoxLayout()
        search_bar = SearchBar(placeholder="Search.....")
        search_layout.addWidget(search_bar)

        self.tasks_layout = QVBoxLayout()

        task1 = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="quiz"
        )

        task2 = TaskCard(
            title="Applied Statistics – Mini Project",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="MHZ4532",
            file_count=2,
            assignment_type="mini_project"
        )

        task3 = TaskCard(
            title="Applied Statistics – Mini Project",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="MHZ4532",
            file_count=2,
            assignment_type="viva"
        )

        self.tasks_layout.addWidget(task1)
        self.tasks_layout.addWidget(task2)
        self.tasks_layout.addWidget(task3)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(self.tasks_layout)
        main_layout.addStretch()

    def update_theme_styles(self):
        self.title.setStyleSheet(f"""
            font-size: 28px; 
            font-weight: bold;
            color: {COLORS.text_primary.name()};
        """)
        