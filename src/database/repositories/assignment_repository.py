from collections.abc import Sequence
from datetime import date as date_type
from datetime import datetime, time, timedelta

from sqlalchemy.orm import Session, joinedload

from src.config.time import APP_TIMEZONE, get_due_soon_days

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
        files: list | None = None,
        description: str = ""
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
            assignment.description = description

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
                description=description
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

    def get_by_date(self, db: Session, selected_date: date_type) -> Sequence[Assignment]:
        """Returns assignments due on a specific date."""

        start = datetime.combine(selected_date, time.min)
        end = start + timedelta(days=1)


        return (
            db.query(Assignment)
            .filter(Assignment.due >= start, Assignment.due < end)
            .order_by(Assignment.due.asc())
            .all()
        )

    def get_due_soon(self, db: Session) -> Sequence[Assignment]:
        """Returns due soon tasks sorted by due date"""

        return (
            db.query(Assignment)
                .filter(
                    Assignment.completed == False,
                    Assignment.due >= datetime.now(APP_TIMEZONE),
                    Assignment.due <= (datetime.now(APP_TIMEZONE) + timedelta(days=get_due_soon_days()))
                )
                .order_by(Assignment.due.asc())
                .all()
        )

    def get_overdue(self, db: Session) -> Sequence[Assignment]:
        """Returns overdue tasks sorted by due dates"""

        return (
            db.query(Assignment)
                .filter(
                    Assignment.completed == False, 
                    Assignment.due < datetime.now(APP_TIMEZONE)
                )
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
