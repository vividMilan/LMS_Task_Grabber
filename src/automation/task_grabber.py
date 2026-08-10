from datetime import datetime


def grabUpcomingEvents(page):
    today = datetime.now().date()

    day_cell_links = []
    headings = []

    calender_section = page.locator('section[data-block="calendar_month"]')

    day_cells = calender_section.locator('td.hasevent')
    total_days = day_cells.count()

    print(f"[*] Total days with events: {total_days}")

    for day_cell in day_cells.all():
        day_link = day_cell.locator('a[data-action="view-event"]')

        day_cell_links.append(day_link.get_attribute("href"))


    for link in day_cell_links:
        page.goto(link, wait_until="domcontentloaded")

        course = page.locator('h1').first.inner_text().strip()

        courseCode = course.split(" ", 1)[0]
        courseName = course.split(" ", 1)[1]

        heading = page.locator('h2').first.inner_text().strip()

        print(f"[*] | Course: {courseName} ({courseCode}) | Event: {heading}")

        # heading = page.locator('h2').inner_text().strip()
        # headings.append(heading)


    for heading in headings:
        print(f"[*] Event: {heading}")