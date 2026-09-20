from datetime import datetime
from zoneinfo import ZoneInfo

from src.automation.schemas import ScrapedFile, ScrappedAssignment
from src.database.models import AssignmentType
from src.utils.assignment_type import assignment_type
from src.utils.date_parser import parse_due_date, parse_viva_time
from src.utils.download_file import download_file
from src.utils.extract_course import extract_course

local_timezone = ZoneInfo("Asia/Colombo")


def grabUpcomingEvents(page):

    today = datetime.now(local_timezone).date()

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

        # Add if the link is not in the array

        href = link.get_attribute("href")

        if href and href not in day_cell_links:
            day_cell_links.append(href)

    for link in day_cell_links:
        page.goto(link, wait_until="domcontentloaded")

        due_div = page.locator("xpath=//div[@data-region='activity-dates']/div[2]")

        if due_div.count() == 0:
            continue

        courseCode, courseName = extract_course(page)

        heading = page.locator("h2").first.inner_text().strip()

        # Skip if submitted
        cell = page.locator("table td").first
        if cell.count() > 0:
            submitted = cell.inner_text().strip().lower()
            if "submitted" in submitted:
                print(f"Skipped for {heading}: {link}")
                continue

        type = assignment_type(heading)

        scraped_task = ScrappedAssignment()

        raw_due = due_div.inner_text()

        file_locators = page.locator(
            "a[href*='pdf'], "
            "a[href*='xls'], "
            "a[href*='xlsx'], "
            "a[href*='doc'], "
            "a[href*='docx']"
        )

        question_files = file_locators.all()
        scraped_files = []

        has_file_upload = len(question_files) > 0

        if has_file_upload:
            for question_file in question_files:
                file_link = question_file.get_attribute("href")

                save_dir = f"downloads/{courseCode}"
                local_path = download_file(page, file_link, output_dir=save_dir)

                scraped_files.append(
                    ScrapedFile(
                        file_link=file_link,
                        file_path=local_path
                    )
                )

                scraped_task.files = scraped_files

        if type == AssignmentType.VIVA_SLOT:
            your_selection = (
                page.locator("xpath=//div[@id='yourselection']").inner_text().strip()
            )
            viva_times = parse_viva_time(your_selection)

            if viva_times:
                scraped_task.start_time, scraped_task.end_time = viva_times
            else:
                print("[!] Unable to get viva selections, please visit the LMS")

        scraped_task.course_id = courseCode
        scraped_task.course_name = courseName
        scraped_task.heading = heading
        scraped_task.link = link
        scraped_task.due_date = parse_due_date(raw_due)
        scraped_task.type = type

        assignments.append(scraped_task)

    return assignments
