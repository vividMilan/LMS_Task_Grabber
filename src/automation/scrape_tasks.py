import os

from dotenv import load_dotenv

from src.automation.auth import login
from src.automation.browser import launch_browser
from src.automation.task_grabber import grabUpcomingEvents
from src.database.connection import SessionLocal
from src.services.credential_service import get_credentials
from src.services.sync_service import process_and_save_scraped_assignment

from PyQt6.QtWidgets import QMessageBox

load_dotenv()

def scrape_tasks():

    username, password = get_credentials()
    
    if not password or not username:
        return False, "Please configure username and password in settings"
    
    url = os.getenv("LMS_URL")

    if not url:
        return False, "LMS url is not configured"

    p, browser, page = launch_browser()
    db = SessionLocal()

    try:

        login_success = login(page, username, password, url)

        if not login_success:
            return (
                False,
                "LMS login failed, Please check your credentials"
            )    
            
        scraped_assignments = grabUpcomingEvents(page)
        count = process_and_save_scraped_assignment(
            db=db, scraped_items=scraped_assignments
        )
        print(f"Count: ${count}")

        return (
            True,
            f"{count} task synced successfully!"
        )
    
    except Exception as e:
        print(f"Sync error: {e}")
        
        return (
            False, 
            str(e)
        )
    finally:
        browser.close()
        p.stop()
        db.close()