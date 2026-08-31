import qtawesome as qta
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.automation.scrape_tasks import scrape_tasks
from src.ui.components.sidebar import Sidebar
from src.ui.components.spinner import Spinner
from src.ui.views.calander_view import CalendarView
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

        # Central Root Widgets & Main horizontal Layout
        root_widget = QWidget()
        self.setCentralWidget(root_widget)
        main_layout = QHBoxLayout(root_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.switch_page)

        # Main area (stacked widget)
        self.content_stack = QStackedWidget()

        page_dashboard = QWidget()
        dash_layout = QVBoxLayout(page_dashboard)
        dash_layout.addWidget(QLabel("Dashboard View"))


        self.btn_sync = QPushButton("Sync Task")
        self.btn_sync.setIcon(qta.icon("fa5s.sync-alt", color="#fffff"))
        self.btn_sync.clicked.connect(self.start_sync_process)

        self.spinner = Spinner(self, size=24, width=3)
        self.spinner.hide()

        dash_layout.addWidget(self.spinner)
        dash_layout.addWidget(self.btn_sync)
        

        page_tasks = TasksView()

        page_calender = CalendarView()

        page_settings = QWidget()
        settings_layout = QVBoxLayout(page_settings)
        settings_layout.addWidget(QLabel("Settings View"))

        # add to the stack
        self.content_stack.addWidget(page_dashboard)
        self.content_stack.addWidget(page_tasks)
        self.content_stack.addWidget(page_calender)
        self.content_stack.addWidget(page_settings)

        # add to main layout & apply styles
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack)

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