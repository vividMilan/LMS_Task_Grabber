from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton, QFrame, QHBoxLayout, QStackedWidget, QLabel
from PyQt6.QtCore import QSize, Qt
import qtawesome as qta

from src.automation.scrape_tasks import scrape_tasks

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
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(200)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(10)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_tasks = QPushButton("Tasks")
        self.btn_settings = QPushButton("Settings")

        for btn in (self.btn_dashboard, self.btn_tasks, self.btn_settings):
            btn.setCheckable(True)
            sidebar_layout.addWidget(btn)


        # Button group event binding
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        self.btn_tasks.clicked.connect(lambda: self.switch_page(1))
        self.btn_settings.clicked.connect(lambda: self.switch_page(2))

        self.btn_dashboard.setChecked(True)

        # Main area (stacked widget)
        self.content_stack = QStackedWidget()

        page_dashboard = QWidget()
        dash_layout = QVBoxLayout(page_dashboard)
        dash_layout.addWidget(QLabel("Dashboard View"))


        self.btn_sync = QPushButton("Sync Task")
        self.btn_sync.setIcon(qta.icon("fa5s.sync-alt", color="#fffff"))
        self.btn_sync.clicked.connect(self.scrape_tasks)
        dash_layout.addWidget(self.btn_sync)

        page_tasks = QWidget()
        page_layout = QVBoxLayout(page_tasks)
        page_layout.addWidget(QLabel("Tasks View"))

        page_settings = QWidget()
        settings_layout = QVBoxLayout(page_settings)
        settings_layout.addWidget(QLabel("Settings View"))

        # add to the stack
        self.content_stack.addWidget(page_dashboard)
        self.content_stack.addWidget(page_tasks)
        self.content_stack.addWidget(page_settings)

        # add to main layout & apply styles
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack)

    def switch_page(self, index: int):
        self.content_stack.setCurrentIndex(index)
        self.btn_dashboard.setChecked(index == 0)
        self.btn_tasks.setChecked(index == 1)
        self.btn_settings.setChecked(index == 2)

    def scrape_tasks(self):
        print("starting scraping....")
        scrape_tasks()