from .base_repository import BaseRepository
from sqlalchemy.orm import Session
from ..models import Course

class CourseRepository(BaseRepository[Course]):

    def __init__(self):
        super().__init__(Course)

    def upsert_course(self, db: Session, course_id: str, name: str, excluded: bool = False) -> Course:
        """Creates a course if missing, or updates its name if present."""
        course = self.get_by_id(db, course_id)

        if course:
            course.name = name
        else:
            course = Course(id=course_id, name = name, excluded = excluded)
            db.add(course)

        db.commit()
        db.refresh(course)
        return course

    def toggle_exclusion(self, db: Session, course_id: str, excluded: bool) -> bool:
        """Toggles whether a course should be skipped during scraping."""
        course = self.get_by_id(db, course_id)

        if course:
            course.excluded = excluded
            db.commit()
            return True

        return False

course_repo = CourseRepository()