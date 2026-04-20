from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStackedWidget
from .components.sidebar import Sidebar
from .pages.home import HomePage
from .pages.calendar import CalendarPage
from .pages.settings import SettingsPage

class MainWindow(QMainWindow):
    
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("LMS Task Grabber")
        self.setMinimumSize(1200, 800)

        # Main Widget and Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)

        # content area for pages
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("background-color: white;")

        # Create pages
        self.home_page = HomePage()
        self.calendar_page = CalendarPage()
        self.settings_page = SettingsPage()

        # Add pages to content area
        self.content_area.addWidget(self.home_page)
        self.content_area.addWidget(self.calendar_page)
        self.content_area.addWidget(self.settings_page)


        self.content_area.setCurrentWidget(self.home_page)

        self.main_layout.addWidget(self.content_area)

        self.sidebar.home_button.clicked.connect(lambda: self.switch_page(0))
        self.sidebar.calendar_button.clicked.connect(lambda: self.switch_page(1))
        self.sidebar.settings_button.clicked.connect(lambda: self.switch_page(2))

    def switch_page(self, page_index):
        self.content_area.setCurrentIndex(page_index)




