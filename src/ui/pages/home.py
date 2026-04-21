from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QFrame,
    QHBoxLayout,
    QScrollArea,
    QCalendarWidget,
)
from PyQt6.QtCore import Qt
import qtawesome as qta
from ui.theme import Theme
from db.session import get_db
from db.repository import AssignmentRepository
from ui.components.task_list import TaskList

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(24, 24, 24, 24)
        page_layout.setSpacing(20)

        self.tasks = self._load_tasks()

        page_layout.addWidget(self._build_search_bar())
        page_layout.addWidget(self._build_header())
        page_layout.addWidget(
            TaskList(self.tasks)
        )
        



    def _build_search_bar(self):

        search_container = QFrame()
        search_container.setObjectName("searchBar")
        search_container.setFixedHeight(48)
        search_container.setContentsMargins(4, 0, 4, 0)
        search_container.setStyleSheet(
            f"""
            QFrame#searchBar {{
                background-color: {Theme.Colors.SEARCH_BG};
                border-radius: 24px;
            }}

            QFrame#searchBar:focus-within {{
                border: 2px solid {Theme.Colors.PRIMARY};
            }}
            """
        )

        search_layout = QHBoxLayout(search_container)
        
        search_icon = QLabel()
        search_icon.setPixmap(qta.icon("fa5s.search", color=Theme.Colors.TEXT_MUTED).pixmap(20, 20))
        search_icon.setObjectName("searchIcon")
        search_icon.setStyleSheet(
            f"""
                QLabel#searchIcon {{
                    background-color: transparent;
                }}
            """
        )

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by course code or date")
        search_input.setFont(Theme.get_font(Theme.Fonts.NORMAL))
        search_input.setStyleSheet(
            f"""
            QLineEdit {{
                border: none;
                background-color: transparent;
                color: {Theme.Colors.TEXT_DARK};
            }}
            """
        )

        search_layout.addWidget(search_icon)
        search_layout.addWidget(search_input)

        return search_container

    def _build_header(self):
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        label = QLabel("Upcoming Tasks")
        label.setFont(Theme.get_font(Theme.Fonts.XLARGE, bold=True))
        label.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")

        header_layout.addWidget(label)
        header_layout.addStretch()
        return header

    def _load_tasks(self):
        try:
            with get_db() as db_session:
                repo = AssignmentRepository(db_session)
                return repo.get_all_assignments()
        except Exception as e:
            print(f"Database Error: {e}")
            return []
    


