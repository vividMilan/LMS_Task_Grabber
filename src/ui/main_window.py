import qtawesome as qta
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.automation.scrape_tasks import scrape_tasks
from src.ui.components.spinner import Spinner

INACTIVE_ICON_COLOR = "#ee5e0b"  # Default orange icon
ACTIVE_ICON_COLOR = "#ffffff"    # White icon when checked/hovered

class ScrapperWorker(QThread):
    finished_signal = pyqtSignal(bool, str) # Emits success status and message

    def run(self):
        try:
            scrape_tasks()
            self.finished_signal.emit(True, "Tasks sysnced successfully!")
        except Exception as e:
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

        # sidebar container

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(6)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        home_icon = qta.icon(
            "ei.home",
            color=INACTIVE_ICON_COLOR,
            color_active=ACTIVE_ICON_COLOR,
            color_selected=ACTIVE_ICON_COLOR
        )

        calender_icon = qta.icon(
            "fa5s.calendar-alt",
            color=INACTIVE_ICON_COLOR,
            color_active=ACTIVE_ICON_COLOR,
            color_selected=ACTIVE_ICON_COLOR
        )

        tasks_icon = qta.icon(
            "ri.todo-fill", 
            color=INACTIVE_ICON_COLOR,
            color_active=ACTIVE_ICON_COLOR,
            color_selected=ACTIVE_ICON_COLOR
        )

        settings_icon = qta.icon(
            "ph.gear-fill",  
            color=INACTIVE_ICON_COLOR,
            color_active=ACTIVE_ICON_COLOR,
            color_selected=ACTIVE_ICON_COLOR
        )

        self.btn_dashboard = QPushButton(home_icon, "")
        self.btn_tasks = QPushButton(tasks_icon, "")
        self.btn_calender = QPushButton(calender_icon, "")
        self.btn_settings = QPushButton(settings_icon, "")


        for btn in (self.btn_dashboard, self.btn_tasks, self.btn_calender, self.btn_settings):
            btn.setCheckable(True)
            sidebar_layout.addWidget(btn)


        # Button group event binding
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.btn_tasks.clicked.connect(lambda: self.switch_page(1))
        self.btn_calender.clicked.connect(lambda: self.switch_page(2))
        self.btn_settings.clicked.connect(lambda: self.switch_page(3))

        self.btn_dashboard.setChecked(True)

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
        

        page_tasks = QWidget()
        page_layout = QVBoxLayout(page_tasks)
        page_layout.addWidget(QLabel("Tasks View"))

        page_calender = QWidget()
        settings_layout = QVBoxLayout(page_calender)
        settings_layout.addWidget(QLabel("Calender View"))

        page_settings = QWidget()
        settings_layout = QVBoxLayout(page_settings)
        settings_layout.addWidget(QLabel("Settings View"))

        # add to the stack
        self.content_stack.addWidget(page_dashboard)
        self.content_stack.addWidget(page_tasks)
        self.content_stack.addWidget(page_calender)
        self.content_stack.addWidget(page_settings)

        # add to main layout & apply styles
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)

    def switch_page(self, index: int):
        self.content_stack.setCurrentIndex(index)
        self.btn_dashboard.setChecked(index == 0)
        self.btn_tasks.setChecked(index == 1)
        self.btn_calender.setChecked(index == 2)
        self.btn_settings.setChecked(index == 3)

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