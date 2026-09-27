import qtawesome as qta
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.database.connection import SessionLocal
from src.database.repositories.assignment_repository import assignment_repo
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

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        header_layout = QHBoxLayout()
        self.title = QLabel("Upcoming Tasks")

        # Sync Button
        self.btn_sync = QPushButton("Sync Tasks")
        self.btn_sync.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_sync.setObjectName("syncButton")
        self.btn_sync.setIcon(qta.icon("fa5s.sync-alt", color="#ffffff"))

        self.btn_sync.clicked.connect(
            self.sync_requested.emit
        )

        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_sync)

        search_layout = QHBoxLayout()
        search_bar = SearchBar(placeholder="Search.....")
        search_layout.addWidget(search_bar)

        self.tasks_layout = QVBoxLayout()

        main_layout.addLayout(header_layout)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(self.tasks_layout)
        main_layout.addStretch()

    def set_syncing(self, syncing: bool):

        self.btn_sync.setDisabled(syncing)

        if syncing:
            self.btn_sync.setText("Syncing....")
            self.btn_sync.setIcon(
                qta.icon(
                    "fa5s.sync-alt",
                    color="#FFFFFF"
                )
            )

        else:
            self.btn_sync.setText("Sync Tasks")
            self.btn_sync.setIcon(
                qta.icon(
                    "fa5s.sync-alt",
                    color="#FFFFFF"
                )
            )

    def update_theme_styles(self):
        self.title.setStyleSheet(f"""
            font-size: 28px; 
            font-weight: bold;
            color: {COLORS.text_primary.name()};
        """)

    def create_task_card(self, assignment):

        # File count
        file_count = len(
            assignment.files
        )

        # due date
        due_time = ""

        due_date = ""

        if assignment.due:

            due_date = assignment.due.strftime(
                "%d, %h %Y"
            )

            due_time = assignment.due.strftime(
                "%I:%M %p"
            )

        course_name = assignment.course.name  if getattr(assignment, "course", None) else ""

        # Create task card
        task_card = TaskCard(
            title=assignment.name,
            due_date=due_date,
            due_time=due_time,
            course_code=assignment.course_id,
            file_count=file_count,
            assignment_type=assignment.type,
            link=assignment.link,
            description=assignment.description,
            course_name=course_name
        )

        # add task card
        self.tasks_layout.addWidget(
            task_card
        )

        task_card.clicked.connect(
            self.assignment_clicked.emit
        )

    def refresh_tasks(self):
        self.load_assingments()

    def load_assingments(self):

        # Remove existing cards
        while self.tasks_layout.count():

            item = self.tasks_layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

        db = SessionLocal()

        try: 
            assignments = assignment_repo.get_upcoming(db)

            print(
                f"Loaded {len(assignments)} assignments"
            )

            for assignment in assignments:
                self.create_task_card(
                    assignment=assignment
                )

        except Exception as e:
            print(
                f"Error loading assignments: {e}"
            )

        finally:
            db.close()
        