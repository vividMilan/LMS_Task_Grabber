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
from ..theme import Theme
from db.session import get_db
from db.repository import AssignmentRepository

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"background-color: {Theme.Colors.PAGE_BG};")

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(24, 24, 24, 24)
        page_layout.setSpacing(20)

        page_layout.addWidget(self._build_search_bar())
        page_layout.addWidget(self._build_header())
        page_layout.addWidget(self._build_task_list())

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
        header.setStyleSheet(f"background-color: {Theme.Colors.PAGE_BG};")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        label = QLabel("Upcoming Tasks")
        label.setFont(Theme.get_font(Theme.Fonts.XLARGE, bold=True))
        label.setStyleSheet(f"color: {Theme.Colors.TEXT_DARK};")

        header_layout.addWidget(label)
        header_layout.addStretch()
        return header

    def _build_task_list(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)

        tasks = []

        try:
            with get_db() as db_session:
                assignment_repo = AssignmentRepository(db_session)
                tasks = assignment_repo.get_all_assignments()
        except Exception as e:
            print(f"Datbase Error: {e}")
            tasks = []

        if not tasks:
            empty_container = QWidget()
            empty_layout = QVBoxLayout(empty_container)
            empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.setContentsMargins(0, 50, 0, 0)
                    
            message_label = QLabel("No Upcoming Tasks Found")
            message_label.setFont(Theme.get_font(Theme.Fonts.MEDIUM, bold=True))
            message_label.setStyleSheet(f"color: {Theme.Colors.TEXT_MUTED};")
            message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else: 
            for task in tasks:
                content_layout.addWidget(self._create_task_card(task))

        content_layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def _create_task_card(self, task):
        card = QFrame()
        card.setObjectName("taskCard")
        card.setStyleSheet(
            f"""
            QFrame#taskCard {{
                background-color: {Theme.Colors.CARD_BG};
                border-radius: 20px;
                padding: 18px;
            }}
            """
        )

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 12, 18, 12)
        card_layout.setSpacing(8)

        title = QLabel(task.name)
        title.setWordWrap(True)
        title.setFont(Theme.get_font(Theme.Fonts.MEDIUM, bold=True))
        title.setStyleSheet(
            f"""
            color: {Theme.Colors.TEXT_DARK};
            background-color: transparent;
            """
        )
        card_layout.addWidget(title)

        meta_row = QWidget()
        meta_row.setStyleSheet(f"""
            background-color: transparent;
        """)
        meta_layout = QHBoxLayout(meta_row)
        meta_layout.setContentsMargins(0, 0, 0, 0)
        meta_layout.setSpacing(10)

        meta_layout.addWidget(self._create_badge("fa5s.book", task.courseCode))
        meta_layout.addWidget(self._create_badge("fa5s.calendar-alt", task.due_date))
        meta_layout.addWidget(self._create_badge("fa5s.clock", task.due_time))
        meta_layout.addStretch()

        card_layout.addWidget(meta_row)
        return card

    def _create_badge(self, icon_name, text):
        badge = QFrame()

        badge.setStyleSheet(
            f"""
            QFrame {{
                background-color: {Theme.Colors.BADGE_BG};
                border-radius: 24px;
                padding: 8px 12px;
            }}
            QLabel {{
                color: {Theme.Colors.BADGE_TEXT};
            }}
            """
        )

        layout = QHBoxLayout(badge)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        icon = QLabel()
        icon.setPixmap(qta.icon(icon_name, color=Theme.Colors.BADGE_TEXT).pixmap(20, 20))
        layout.addWidget(icon)

        label = QLabel(text)
        label.setFont(Theme.get_font(Theme.Fonts.SMALL, bold=True))
        layout.addWidget(label)

        return badge


