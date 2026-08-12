from datetime import datetime

from utils.date_parser import parse_due_date
from utils.download_file import download_file

def grabUpcomingEvents(page):
    today = datetime.now().date()

    day_cell_links = []

    assignments = []

    calender_section = page.locator('section[data-block="calendar_month"]')

    day_cells = calender_section.locator("td.hasevent")
    total_days = day_cells.count()

    print(f"[*] Total days with events: {total_days}")

    link_locator = day_cells.locator('xpath=//a[@data-action="view-event"]').all()

    for link in link_locator:
        link_date = (
            link.locator('xpath=/../../../../a[@data-action="view-day-link"]/span/span')
            .inner_text()
            .strip()
        )

        if int(link_date) < today.day:
            continue

        if link.get_attribute("href") not in day_cell_links:
            day_cell_links.append(link.get_attribute("href"))

    for link in day_cell_links:
        page.goto(link, wait_until="domcontentloaded")

        due_div = page.locator("xpath=//div[@data-region='activity-dates']/div[2]")

        if due_div.count() == 0:
            continue
        
        course = page.locator("h1").first.inner_text().strip()

        courseCode = course.split(" ", 1)[0]
        courseName = course.split(" ", 1)[1]

        heading = page.locator("h2").first.inner_text().strip()

        raw_text = due_div.inner_text()

        question_files = page.locator("a[href*='pdf']").all()

        has_file_upload = len(question_files) > 0

        if has_file_upload:
            for question_file in question_files:
                file_uri = question_file.get_attribute("href")

                save_dir = f"downloads/{courseCode}"
                local_path = download_file(page, file_uri, output_dir=save_dir)
                
                if local_path:
                    assignment["Question Material"] = local_path

                assignment = {
                    "courseCode": courseCode,
                    "courseName": courseName,
                    "heading": heading,
                    "link": link,
                    "dueDate": parse_due_date(raw_text),
                    "Question Material": local_path or file_uri,
                }


            

            assignments.append(assignment)
        else:
            assignment = {
                "courseCode": courseCode,
                "courseName": courseName,
                "heading": heading,
                "link": link,
                "dueDate": parse_due_date(raw_text),
                "Question Material": None,
            }

            assignments.append(assignment)


    print(f"[*] Total assignments found: {len(assignments)}")

    for assignment in assignments:
        print(
            f"========================{assignment['courseCode']} - {assignment['heading']}========================\n"
            f"Due Date: {assignment['dueDate']}\n"
            f"Link: {assignment['link']}\n"
            f"Question Material: {assignment['Question Material']}\n"
        )
