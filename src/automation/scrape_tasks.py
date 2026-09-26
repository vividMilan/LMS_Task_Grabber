import os

from dotenv import load_dotenv

from src.automation.auth import login
from src.automation.browser import launch_browser
from src.automation.task_grabber import grabUpcomingEvents
from src.database.connection import SessionLocal
from src.services.sync_service import process_and_save_scraped_assignment

from src.services.credential_service import get_credentials

load_dotenv()
username, password = get_credentials()
url = os.getenv("LMS_URL")

print("============ Credentials ===============")
print(username)
print(password)

# if password is None:
#     raise RuntimeError("LMS password has not been set")

def scrape_tasks():
    p, browser, page = launch_browser()
    db = SessionLocal()
    try:
        if login(page, username, password, url):
            scraped_assignments = grabUpcomingEvents(page)
            count = process_and_save_scraped_assignment(
                db=db, scraped_items=scraped_assignments
            )
            print(f"Count: ${count}")
    finally:
        browser.close()
        p.stop()
        db.close()