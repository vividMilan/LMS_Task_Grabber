from datetime import datetime

def grabUpcomingEvents(page):
    # now = datetime.datetime.now()
    # today = now.day

    # calender_section = page.locator('section[data-block="calendar_month"]')

    # day_cells = calender_section.locator('td.hasevent')
    # total_days = day_cells.count()

    # links = set()
    # assignments = []

    # for i in range(total_days):
    #     date = day_cells.nth(i)

    #     date_links = date.locator('div.d-none.d-md-block.hidden-phone.text-xs-center a[data-action="view-event"]')

    #     for j in range(date_links.count()):
    #         links.add(date_links.nth(j).get_attribute("href"))

    # for link in links:

    #     page.goto(link, wait_until="domcontentloaded")

    #     assingment_name = page.locator('section#region-main h2').inner_text().strip()

    #     dates = page.locator('div[data-region="activity-dates"] div')

    #     due_text = dates.nth(1).inner_text().strip()

    #     due_date_str = due_text.split(":", 1)[1].strip()

    #     due_date_obj = datetime.strptime(due_date_str, "%A, %d %B %Y, %I:%M %p")

    #     course = page.locator('h1').inner_text().strip()

    #     courseName = course.split(" ", 1)[1].strip()

    #     courseCode = course.split(" ", 1)[0].strip()

    #     assignments.append({
    #         "name": assingment_name,
    #         "course": courseName,
    #         "courseCode": courseCode,
    #         "due_date": due_date_obj,
    #         "link": link
    #     })

    # return assignments

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