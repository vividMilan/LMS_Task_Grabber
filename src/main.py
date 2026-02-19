from playwright.sync_api import sync_playwright, TimeoutError
from dotenv import load_dotenv
from datetime import datetime
import os
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from model.assignment import Assignment


# Load Environment Variables
load_dotenv()
username = os.getenv("LMS_USERNAME")
password = os.getenv("LMS_PASSWORD")

url = os.getenv("LMS_URL")


def launch_browser():
    """Launches the browser and returns the page object."""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    return p, browser, page

def login(page, username, password):
    """Logs into OUSL LMS via IAM."""
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        print("Opened login page.")

        page.get_by_role("link", name="IAM OUSL LMS USER").click()
        print("Redirecting..")

        page.wait_for_selector('input[name="username"]', timeout=60000)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('input[type="submit"]')
        print("Submitted login credentials.")

        page.wait_for_selector('div[role="listitem"]', timeout=60000)
        print("Logged in successfully!")

    except TimeoutError as e:
        print("Timeout or login failed:", e)
        return False
    except Exception as e:
        print("Login error:", e)
        return False

    return True

def grabUpcomingEvents(page):
    # now = datetime.datetime.now()
    # today = now.day

    calender_section = page.locator('section[data-block="calendar_month"]')

    day_cells = calender_section.locator('td.hasevent')
    total_days = day_cells.count()

    links = set()
    assignments = []

    for i in range(total_days):
        date = day_cells.nth(i)

        date_links = date.locator('div.d-none.d-md-block.hidden-phone.text-xs-center a[data-action="view-event"]')

        for j in range(date_links.count()):
            links.add(date_links.nth(j).get_attribute("href"))

    for link in links:

        page.goto(link, wait_until="domcontentloaded")

        assingment_name = page.locator('section#region-main h2').inner_text().strip()

        dates = page.locator('div[data-region="activity-dates"] div')

        due_text = dates.nth(1).inner_text().strip()

        due_date_str = due_text.split(":", 1)[1].strip()

        due_date_obj = datetime.strptime(due_date_str, "%A, %d %B %Y, %I:%M %p")

        course = page.locator('h1').inner_text().strip()

        assignment = Assignment(assingment_name, course, due_date_obj, link)
        assignment.print_info()
        assignments.append(assignment)

    return assignments

def main():
    p, browser, page = launch_browser()
    try:
        if login(page, username, password):
            grabUpcomingEvents(page)
    finally:
        browser.close()
        p.stop()

if __name__ == "__main__":
    main()
    # app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    # sys.exit(app.exec())
