from playwright.sync_api import sync_playwright, TimeoutError
from dotenv import load_dotenv
import datetime
import os

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
        page.goto(url)
        print("Opened login page.")

        page.get_by_role("link", name="IAM OUSL LMS USER").click()
        print("Redirecting..")

        page.wait_for_selector('input[name="username"]', timeout=5000)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('input[type="submit"]')
        print("Submitted login credentials.")

        page.wait_for_selector('div[role="listitem"]', timeout=5000)
        print("Logged in successfully!")

    except TimeoutError as e:
        print("Timeout or login failed:", e)
        return False
    except Exception as e:
        print("Login error:", e)
        return False

    return True

def grabUpcomingEvents(page):
    now = datetime.datetime.now()
    today = now.day

    calender_section = page.locator('section[data-block="calendar_month"]')

    day_cells = calender_section.locator('td.hasevent')

    for i in range(day_cells.count()):
        cell = day_cells.nth(i)

        date = cell.locator('div.d-none.d-md-block.hidden-phone.text-xs-center span.day-number').inner_text().strip()

        date_link = cell.locator('a[data-action="view-day-link"]').first # grab event link

        date_link.click() # open each event link

        page.wait_for_selector('div[role="main"]') # Wait to date page to load

        events = page.locator('div[data-type="event"]')

        for i in range (events.count()):
            event = events.nth(i)

            event_name = event.locator('h3.name.d-inline-block').inner_text().strip()
            event_links = event.locator('div div.col-11 a')
            event_date_link = event.locator('div div.col-11')

            event_date_time = event_date_link.nth(0).inner_text().split(",")
            event_date = f"{event_date_time[0].strip()}, {event_date_time[1].strip()}"
            event_time = event_date_time[2].strip()
            event_course = event_links.nth(1).inner_text().strip()


            print("\n========================= Assignments =========================")
            print(f"Name : {event_name}")
            print(f"Course : {event_course}")
            print(f"Date : {event_date}")
            print(f"Time : {event_time}")



def printEvents(page, links):
    pass
            

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
