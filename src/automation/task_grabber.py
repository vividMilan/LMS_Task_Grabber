from datetime import datetime

from src.automation.schemas import ScrappedAssignment

from src.utils.date_parser import parse_due_date
from src.utils.download_file import download_file
from src.utils.assignment_type import assignment_type
from src.utils.extract_course import extract_course

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

        # if int(link_date) < today.day:
        #     continue

        if link.get_attribute("href") not in day_cell_links:
            day_cell_links.append(link.get_attribute("href"))

    for link in day_cell_links:
        page.goto(link, wait_until="domcontentloaded")

        due_div = page.locator("xpath=//div[@data-region='activity-dates']/div[2]")

        if due_div.count() == 0:
            continue

        courseCode, courseName = extract_course(page)

        heading = page.locator("h2").first.inner_text().strip()

        type = assignment_type(heading)

        raw_text = due_div.inner_text()

        question_files = page.locator("a[href*='pdf']").all()

        has_file_upload = len(question_files) > 0

        if has_file_upload:
            for question_file in question_files:
                file_uri = question_file.get_attribute("href")

                save_dir = f"downloads/{courseCode}"
                local_path = download_file(page, file_uri, output_dir=save_dir)


                scraped_task = ScrappedAssignment(
                    course_id=courseCode,
                    course_name=courseName,
                    heading=heading,
                    link=link,
                    due_date=parse_due_date(raw_text),
                    file_path=local_path,
                    file_link=file_uri,
                    type=type
                )

            assignments.append(scraped_task)
            
        else:
            scraped_task = ScrappedAssignment(
                course_id=courseCode,
                course_name=courseName,
                heading=heading,
                link=link,
                due_date=parse_due_date(raw_text),
                file_path=None,
                file_link=None,
                type=type
            )

            assignments.append(scraped_task)

    return assignments