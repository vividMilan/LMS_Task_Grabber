from collections.abc import Sequence
from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from ..models import Assignment
from .base_repository import BaseRepository


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
        type: str | None = None,
        files: list | None = None
    ) -> tuple[Assignment, bool]:
        """Inserts or updates an assignment record from scraped task data."""

        assignment = self.get_by_id(db=db, id_val=assignment_id)

        if assignment:
            assignment.name = name
            assignment.course_id = course_id
            assignment.link = link
            assignment.type = type
            assignment.due = due
            assignment.files = files

            return assignment, False
        else:
            assignment = Assignment(
                id=assignment_id,
                name=name,
                course_id=course_id,
                link=link,
                due=due,
                type=type,
                completed=False,
            )

            db.add(assignment)

        db.commit()
        db.refresh(assignment)
        return assignment, True

    def get_upcoming(self, db: Session) -> Sequence[Assignment]:
        """Returns incomplete tasks sorted by due date (eagerly loading course and file)."""
        return (
            db.query(Assignment)
            .options(joinedload(Assignment.course), joinedload(Assignment.files))
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
