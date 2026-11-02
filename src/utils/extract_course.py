from playwright.sync_api import Page


def extract_course(page):
    course = page.locator("h1").first.inner_text().strip()

    courseCode = course.split(" ", 1)[0]
    courseName = course.split(" ", 1)[1]

    return courseCode, courseName



def extract_course_from_legacy(page: Page):

    course_element = page.locator("xpath=//nav/ol/li[1]/a")

    if course_element.count() == 0:
        return None, None

    course_text = course_element.first.inner_text().strip()

    courseCode = course_text.split("_", 1)[0].strip()

    courseName = course_element.get_attribute("title").strip()

    return courseCode, courseName
