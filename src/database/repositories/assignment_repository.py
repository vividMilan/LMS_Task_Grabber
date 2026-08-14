from .base_repository import BaseRepository
from ..models import Assignment
from typing import Optional, Sequence
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

class AssignmentRepository(BaseRepository[Assignment]):
    def __init__(self):
        super().__init__(Assignment)

    def upsert_assignment(
        self,
        db: Session,
        assignment_id: str,
        name: str,
        course_id: str,
        due: datetime,
        link: str,
        file_id: Optional[int] = None,
        type: Optional[str] = None,
    ) -> Assignment:
        """Inserts or updates an assignment record from scraped task data."""

        assignment = self.get_by_id(db, assignment_id)

        if assignment:
            assignment.name = name
            assignment.course_id = course_id
            assignment.link = link
            assignment.file_id = file_id
            assignment.type = type
            assignment.due = due
            if file_id:
                assignment.file_id = file_id
        else:
            assignment = Assignment(
                id=assignment_id,
                name=name,
                course_id=course_id,
                link=link,
                due=due,
                type=type,
                file_id=file_id,
                completed=False
            )

            db.add(assignment)

        db.commit()
        db.refresh(assignment)
        return assignment


    def get_upcoming(self, db: Session) -> Sequence[Assignment]:
        """Returns incomplete tasks sorted by due date (eagerly loading course and file)."""
        return (
            db.query(Assignment)
            .options(
                joinedload(Assignment.course),
                joinedload(Assignment.file)
            )
            .filter(Assignment.completed == False)
            .order_by(Assignment.due.asc())
            .all()
        )

    def mark_completed(self, db: Session, assignment_id: str) -> bool:
        """Marks a task as finished."""

        assignment = self.get_by_id(db, assignment_id)

        if assignment:
            assignment.completed = True
            db.commit()
            return True

        return False

assignment_repo = AssignmentRepository()