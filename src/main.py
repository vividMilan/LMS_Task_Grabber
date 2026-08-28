import os
import sys

from dotenv import load_dotenv
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

def gui_mode():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # cli_mode()
    gui_mode()
