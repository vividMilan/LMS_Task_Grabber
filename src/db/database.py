from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from tabulate import tabulate

# Database setup
DB_NAME = "assignments.db"
engine = create_engine(f'sqlite:///{DB_NAME}', echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Course(Base):
    __tablename__ = "courses"

    code = Column(String, primary_key=True)
    level = Column(String, nullable=True)
    name = Column(String, nullable=False)
    excluded = Column(Boolean, default=False)

    # Relationship
    assignments = relationship("Assignment", back_populates="course_rel")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    course = Column(String, nullable=False)  # Denormalized for display
    courseCode = Column(String, ForeignKey('courses.code'), nullable=False)
    due_date = Column(String, nullable=False)
    due_time = Column(String, nullable=False)
    link = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

    # Relationship
    course_rel = relationship("Course", back_populates="assignments")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def save_assignment(assignment):
    db = get_db()
    try:
        # Check if course exists, create if not
        course = db.query(Course).filter(Course.code == assignment["courseCode"]).first()
        if not course:
            course = Course(code=assignment["courseCode"], name=assignment["course"])
            db.add(course)

        # Create assignment
        new_assignment = Assignment(
            name=assignment["name"],
            course=assignment["course"],
            courseCode=assignment["courseCode"],
            due_date=assignment["due_date"].strftime("%Y-%m-%d"),
            due_time=assignment["due_date"].strftime("%H:%M"),
            link=assignment["link"],
            completed=assignment.get("completed", False)
        )
        db.add(new_assignment)
        db.commit()
    finally:
        db.close()

def print_all_assignments():
    db = get_db()
    try:
        assignments = db.query(Assignment).all()

        if not assignments:
            print("No assignments found in the database.")
            return

        # Prepare data for tabulate
        rows = []
        for assignment in assignments:
            rows.append([
                assignment.id,
                assignment.name,
                assignment.course,
                assignment.courseCode,
                assignment.due_date,
                assignment.due_time,
                assignment.link,
                assignment.completed
            ])

        headers = ["ID", "Name", "Course", "Course Code", "Due Date", "Due Time", "Link", "Completed"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    finally:
        db.close()

def print_all_courses():
    db = get_db()
    try:
        courses = db.query(Course).all()

        if not courses:
            print("No courses found in the database.")
            return

        # Prepare data for tabulate
        rows = []
        for course in courses:
            rows.append([
                course.code,
                course.name,
                course.excluded
            ])

        headers = ["Course Code", "Course Name", "Excluded"]
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    finally:
        db.close()