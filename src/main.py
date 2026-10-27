
import os
import sys

from dotenv import load_dotenv
from PyQt6.QtCore import QFileSystemWatcher
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from src.automation.auth import login
from src.automation.browser import launch_browser
from src.automation.task_grabber import grabUpcomingEvents
from src.config.resource_path import resource_path
from src.database.connection import SessionLocal, init_db
from src.services.sync_service import process_and_save_scraped_assignment
from src.ui.main_window import MainWindow

init_db()

# Load Environment Variables
load_dotenv()
username = os.getenv("LMS_USERNAME")
password = os.getenv("LMS_PASSWORD")
url = os.getenv("LMS_URL")


def cli_mode():
    """Runs the script in CLI mode."""
    print("Running in CLI mode...")

    p, browser, page = launch_browser()
    db = SessionLocal()
    try:
        if login(page, username, password, url):
            scraped_assignments = grabUpcomingEvents(page)
            count = process_and_save_scraped_assignment(
                db=db, scraped_items=scraped_assignments
            )
            print(f"Hello: {count}")
    finally:
        browser.close() 
        p.stop()
        db.close()

class QSSWatcher:
    def __init__(self, app: QApplication):
        self.app = app
        self.qss_path = resource_path("src/ui/styles/style.qss")

        if not self.qss_path.exists():
            raise FileNotFoundError(
                f"Stylesheet not found: {self.qss_path}"
            )
                
        self.watcher = QFileSystemWatcher([str(self.qss_path)])
        self.watcher.fileChanged.connect(self.reload_styles)
        
        self.reload_styles()

    def reload_styles(self):
        if self.qss_path.exists():
            with open(self.qss_path, "r", encoding="utf-8") as f:
                self.app.setStyleSheet(f.read())
            print("[QSS] Stylesheet reloaded.")

def gui_mode():
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    icon_path = resource_path("assets/logo.png")

    app.setWindowIcon(QIcon(str(icon_path)))
    _qss_watcher = QSSWatcher(app)
    
    window = MainWindow()

    if window.should_start_minimized():
        window.showMinimized()
    else:
        window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    # cli_mode()
    gui_mode()
