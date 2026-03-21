from playwright.sync_api import sync_playwright, TimeoutError
from dotenv import load_dotenv
import os
import db.database as database
from automation.auth import login
from automation.browser import launch_browser
from automation.task_grabber import grabUpcomingEvents

database.init_db()

# Load Environment Variables
load_dotenv()
username = os.getenv("LMS_USERNAME")
password = os.getenv("LMS_PASSWORD")

url = os.getenv("LMS_URL")

def main():
    p, browser, page = launch_browser()
    try:
        if login(page, username, password, url):
            assignments = grabUpcomingEvents(page)
            for assignment in assignments:
                database.save_assignment(assignment)

            database.print_all_assignments()
            database.print_all_courses()
    finally:
        browser.close()
        p.stop()

if __name__ == "__main__":
    main()