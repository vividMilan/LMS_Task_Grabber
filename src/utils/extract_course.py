def extract_course(page):
    course = page.locator("h1").first.inner_text().strip()

    courseCode = course.split(" ", 1)[0]
    courseName = course.split(" ", 1)[1]

    return courseCode, courseName
