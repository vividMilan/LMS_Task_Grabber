import os

from dotenv import load_dotenv

from automation.auth import login
from automation.browser import launch_browser
from automation.task_grabber import grabUpcomingEvents

# Load Environment Variables
load_dotenv()
username = os.getenv("LMS_USERNAME")
password = os.getenv("LMS_PASSWORD")
url = os.getenv("LMS_URL")


def cli_mode():
    """Runs the script in CLI mode."""
    print("Running in CLI mode...")

    p, browser, page = launch_browser()
    try:
        if login(page, username, password, url):
            grabUpcomingEvents(page)
    finally:
        browser.close()
        p.stop()


if __name__ == "__main__":
    cli_mode()
