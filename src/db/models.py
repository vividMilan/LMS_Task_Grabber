from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship    

Base = declarative_base()

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
    link = Column(String, nullable=False, unique=True)
    completed = Column(Boolean, default=False)

    # Relationship
    course_rel = relationship("Course", back_populates="assignments")