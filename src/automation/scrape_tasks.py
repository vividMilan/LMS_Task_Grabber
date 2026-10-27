import os

from dotenv import load_dotenv
from playwright.sync_api import Error as PlaywrightError
from sqlalchemy.exc import SQLAlchemyError

from src.automation.auth import login
from src.automation.browser import launch_browser
from src.automation.task_grabber import grabUpcomingEvents
from src.database.connection import SessionLocal
from src.services.credential_service import get_credentials
from src.services.sync_service import process_and_save_scraped_assignment

load_dotenv()

def scrape_tasks() -> tuple[bool, str]:

    """Scrape LMS assignments and save them to the database."""

    username, password = get_credentials()
    
    if not password or not username:
        return False, "Please configure username and password in settings"
    
    url = os.getenv("LMS_URL")

    if not url:
        return False, "LMS url is not configured"

    p = None
    browser = None
    db = None


    try:

        # create the database session
        db = SessionLocal()

        # Launch Playwright
        p, browser, page = launch_browser()

        # Authenticate
        login_success = login(page, username, password, url)

        if not login_success:
            return (
                False,
                "LMS login failed, Please check your credentials"
            )    

        # Scrape Assignments
        scraped_assignments = grabUpcomingEvents(page)

        # Save assignments
        stats = process_and_save_scraped_assignment(
            db=db, scraped_items=scraped_assignments
        )

        # commit if repository methods do not commit internally
        db.commit()

        message = (
            f"Sync Completed: {stats['created']} created, "
            f"{stats['updated']} updated, "
            f"{stats['total']} processed."
        )

        return True, message
    
    except (PlaywrightError, SQLAlchemyError) as e:
        if db is not None:
            db.close()

        print(f"Sync error: {e}")

        return False, f"Assignment sync failed: {e}"
    finally:
        if db is not None:
            db.close()

        if browser is not None:
            try:
                browser.close()
            except PlaywrightError as e:
                print(f"Browser cleanup error: {e}")

        if p is not None:
            try:
                p.stop()
            except PlaywrightError as e:
                print(f"Playwright cleanup error: {e}")