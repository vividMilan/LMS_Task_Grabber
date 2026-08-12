from datetime import datetime
from utils.date_parser import parse_due_date

def grabUpcomingEvents(page):
    today = datetime.now().date()

    day_cell_links = []

    assignments = []

    calender_section = page.locator('section[data-block="calendar_month"]')

    day_cells = calender_section.locator('td.hasevent')
    total_days = day_cells.count()

    print(f"[*] Total days with events: {total_days}")

    link_locator = page.locator('xpath=//a[@data-action="view-event"]').all()

    for link in link_locator:
        if link.get_attribute("href") not in day_cell_links:
            day_cell_links.append(link.get_attribute("href"))




    for link in day_cell_links:
        page.goto(link, wait_until="domcontentloaded")

        course = page.locator('h1').first.inner_text().strip()

        courseCode = course.split(" ", 1)[0]
        courseName = course.split(" ", 1)[1]

        heading = page.locator('h2').first.inner_text().strip()

        due_div = page.locator("xpath=//div[@data-region='activity-dates']/div[2]")

        if (due_div.count() == 0):
            continue
        
        raw_text = due_div.inner_text()

        assignment = {
            "courseCode": courseCode,
            "courseName": courseName,
            "heading": heading,
            "link": link,
            "dueDate": parse_due_date(raw_text)
        }

        assignments.append(assignment)

    print(f"[*] Total assignments found: {len(assignments)}")
    
    for assignment in assignments:
        print(f"[*] {assignment['courseCode']} - {assignment['heading']} - Due: {assignment['dueDate']} | Link: {assignment['link']}")
