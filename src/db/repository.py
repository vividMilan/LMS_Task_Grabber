from .models import Assignment, Course
from tabulate import tabulate
from PyQt6.QtCore import QDate  
from datetime import datetime    

class AssignmentRepository:
    
    def __init__(self, session):
        self.db = session

    def save_assignment(self, assignment):
        """Saves an assignment to the database"""

        course = self.db.query(Course).filter(Course.code == assignment["courseCode"]).first()

        if not course:
            course = Course(code=assignment["courseCode"], name=assignment["course"], level=assignment["courseCode"][3])
            self.db.add(course)

        existing_assignment = self.db.query(Assignment).filter(Assignment.link == assignment["link"]).first()

        if not existing_assignment:
            new_assignment = Assignment(
                name=assignment["name"],
                course=assignment["course"],
                courseCode=assignment["courseCode"],
                due_date=assignment["due_date"].strftime("%Y-%m-%d"),
                due_time=assignment["due_date"].strftime("%H:%M"),
                link=assignment["link"],
                completed=assignment.get("completed", False)
            )
            self.db.add(new_assignment)
            self.db.commit()
        

    def print_all_assignments(self):
        assignments = self.db.query(Assignment).all()

        row = [[t.id, t.name, t.course, t.courseCode, t.due_date, t.due_time, t.link, t.completed] for t in assignments]

        print(tabulate(row, headers=["ID", "Name", "Course", "Course Code", "Due Date", "Due Time", "Link", "Completed"], tablefmt="grid"))
    
    def print_all_courses(self):
        courses = self.db.query(Course).all()

        row = [[t.code, t.name, t.level, t.excluded] for t in courses]

        print(tabulate(row, headers=["Code", "Name", "Level", "Excluded"], tablefmt="grid"))

    def get_all_assignments(self):
        """Returns all assignments as ORM objects"""
        return self.db.query(Assignment).all()
    
    def get_assignment_by_date(self, date):

        if not isinstance(date, str):
            date = date.strftime("%Y-%m-%d")

        return self.db.query(Assignment).filter(Assignment.due_date == date).all()

    def get_all_assignment_date(self):
        result = self.db.query(Assignment.due_date).distinct().all()

        dates = []

        for row in result:
            if row[0]:
                dt = datetime.strptime(row[0], "%Y-%m-%d")
                print(f"{dt.year}-{dt.month}-{dt.day}")
                dates.append(QDate(dt.year, dt.month, dt.day))

        print(dates)

        return dates