
import os
import sys
from pathlib import Path

from PyQt6.QtGui import QIcon

from dotenv import load_dotenv
from PyQt6.QtCore import QFileSystemWatcher
from PyQt6.QtWidgets import QApplication

from src.automation.auth import login
from src.automation.browser import launch_browser
from src.automation.task_grabber import grabUpcomingEvents
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
    def __init__(self, app: QApplication, qss_relative_path: str):
        self.app = app
        self.qss_path = Path(__file__).resolve().parent / qss_relative_path
        
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
    app.setWindowIcon(QIcon("assets/logo.png"))
    _qss_watcher = QSSWatcher(app, "ui/styles/style.qss")
    window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # cli_mode()
    gui_mode()
