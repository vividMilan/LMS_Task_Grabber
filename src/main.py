from dotenv import load_dotenv
import os
from db.repository import AssignmentRepository
from db.session import init_db, get_db
from automation.auth import login
from automation.browser import launch_browser
from automation.task_grabber import grabUpcomingEvents

# GUI imports
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.theme import Theme

# Setup DB + env
init_db()

# Load Environment Variables
load_dotenv()
username = os.getenv("LMS_USERNAME")
password = os.getenv("LMS_PASSWORD")
url = os.getenv("LMS_URL")


def cli_main():
    # legacy CLI mode
    with get_db() as db_session:
        AssignmentRepo = AssignmentRepository(db_session)

        p, browser, page = launch_browser()
        try:
            if login(page, username, password, url):
                assignments = grabUpcomingEvents(page)
                for assignment in assignments:
                    AssignmentRepo.save_assignment(assignment)

                AssignmentRepo.print_all_assignments()
        finally:
            browser.close()
            p.stop()


def gui_main():
    app = QApplication([])
    Theme.Fonts.load_fonts()  # Load custom fonts
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    # default to GUI; use CLI by setting CLI_MODE=1 or cmd arg --cli
    import sys
    gui_main()