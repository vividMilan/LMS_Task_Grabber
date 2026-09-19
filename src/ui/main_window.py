import qtawesome as qta
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QWidget,
)

from src.automation.scrape_tasks import scrape_tasks
from src.ui.components.sidebar import Sidebar
from src.ui.components.spinner import Spinner
from src.ui.styles.tokens import COLORS
from src.ui.views.assignment_view import AssignmentView
from src.ui.views.calander_view import CalendarView
from src.ui.views.dashboard_view import DashboardView
from src.ui.views.setting_view import SettingsView
from src.ui.views.tasks_view import TasksView


class ScrapperWorker(QThread):
    finished_signal = pyqtSignal(bool, str) # Emits success status and message

    def run(self):
        try:
            scrape_tasks()
            self.finished_signal.emit(True, "Tasks sysnced successfully!")
        except Exception as e: # noqa: BLE001
            self.finished_signal.emit(False, str(e))

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LMS Tracker")
        self.setGeometry(100, 200, 1200, 700)

        self._init_ui()
        
        

    def _init_ui(self):
        # Central Root Widgets & Main horizontal Layout
        self.root_widget = QWidget()
        self.setCentralWidget(self.root_widget)
        main_layout = QHBoxLayout(self.root_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.switch_page)

        # Main area (stacked widget)
        self.content_stack = QStackedWidget()

        self.page_dashboard = DashboardView()

        self.btn_sync = QPushButton("Sync Task")
        self.btn_sync.setIcon(qta.icon("fa5s.sync-alt", color="#fffff"))
        self.btn_sync.clicked.connect(self.start_sync_process)

        self.spinner = Spinner(self, size=24, width=3)
        self.spinner.hide()


        # ======================
        # PAGES
        # ======================
        self.page_tasks = TasksView()
        self.page_assignment_view = AssignmentView()
        self.page_calender = CalendarView()
        self.page_settings = SettingsView()

        # =======================
        # Assignment Navigation
        # =======================

        self.page_tasks.assignment_clicked.connect(
            self.open_assignment
        )

        self.page_assignment_view.back_requested.connect(
            self.show_tasks
        )

        # add to the stack
        self.content_stack.addWidget(self.page_dashboard)
        self.content_stack.addWidget(self.page_tasks)
        self.content_stack.addWidget(self.page_calender)
        self.content_stack.addWidget(self.page_settings)
        self.content_stack.addWidget(self.page_assignment_view)

        # add to main layout & apply styles
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack)

        self.apply_styles()

    def switch_page(self, index: int):
        self.content_stack.setCurrentIndex(index)
        
    def start_sync_process(self):
        self.btn_sync.setDisabled(True)

        self.worker = ScrapperWorker()
        self.worker.finished_signal.connect(self.on_sync_finished)

        self.spinner.start()
        self.worker.start()

    def on_sync_finished(self, success: bool, message: str):
        self.btn_sync.setDisabled(False)
        self.spinner.stop()


        if success:
            self.btn_sync.setText(f"Sucess: {message}")
        else:
            self.btn_sync.setText(f"Failed: {message}")

    def open_assignment(self, task):
        print(
            "Opening assignment:",
            task.title
        )

        # Give the selected taskCard to AssingmentView
        self.page_assignment_view.set_assignment(
            task
        )

        # Switch Page
        self.content_stack.setCurrentWidget(
            self.page_assignment_view
        )

    def switch_page(self, index: int):
        self.content_stack.setCurrentIndex(
            index
        )

    def show_tasks(self):
        self.content_stack.setCurrentWidget(
            self.page_tasks
        )

    def apply_styles(self):
        self.root_widget.setObjectName("centralWidget")
        self.root_widget.setStyleSheet(f"""
            QWidget#centralWidget {{
                background-color: {COLORS.window_bg.name()};
                color: {COLORS.text_primary.name()};
            }}
        """)
