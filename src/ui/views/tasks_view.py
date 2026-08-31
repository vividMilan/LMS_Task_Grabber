from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt6.QtCore import Qt

from src.ui.components.search_bar import SearchBar
from src.ui.components.task_card import TaskCard

import qtawesome as qta

class TasksView(QWidget):
    def __init__(
        self, 
        parent = None
    ):
        super().__init__(parent)
        self.setObjectName("taskView")
        self._init_ui()


    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Header Layout

        header_layout = QHBoxLayout()

        tasks_layout = QVBoxLayout()

        # Heading
        title = QLabel("Upcoming Tasks")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        # Sync Button
        btn_sync = QPushButton("Sync Tasks")
        btn_sync.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_sync.setObjectName("syncButton")
        btn_sync.setIcon(qta.icon("fa5s.sync-alt", color="#ffffff"))

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(btn_sync)

        # Search Box
        search_layout = QHBoxLayout()
        search_bar = SearchBar(placeholder="Search.....")
        search_layout.addWidget(search_bar)

        # Tasks
        task = TaskCard(
            title="Database Management – TMA 01",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="EEX5432",
            assignment_type="TMA"
        )

        task2 = TaskCard(
            title="Applied Statistics – Mini Project",
            due_date="2026/08/12",
            due_time="11:59PM",
            course_code="MHZ4532",
            file_count=2,
            assignment_type="Mini Project"
        )

        tasks_layout.addWidget(task)
        tasks_layout.addWidget(task2)

        
        main_layout.addLayout(header_layout)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(tasks_layout)
        main_layout.addStretch()




        
