from datetime import datetime, timedelta

from src.config.time import APP_TIMEZONE, get_due_soon_days
from src.database.connection import SessionLocal
from src.database.models import Assignment


def check_deadlines() -> dict:

    print("Deadline check started!")

    due_soon_days = get_due_soon_days()

    now = datetime.now(APP_TIMEZONE)
    due_soon_limit = now + timedelta(days=due_soon_days)

    overdue = []
    due_soon = []

    with SessionLocal() as db:
        assignments = db.query(Assignment).all()

        for assignment in assignments:

            # Ignore if completed
            if assignment.completed:
                continue

            if not assignment.due:
                continue

            # SQLite often returns naive datetimes.
            # Treat these as Colombo local time.

            due = assignment.due

            if due.tzinfo is None:
                due = due.replace(tzinfo=APP_TIMEZONE)

            else:
                due = due.astimezone(APP_TIMEZONE)

            if due < now:
                overdue.append(assignment.name)
            elif now <= due <= due_soon_limit:
                due_soon.append(assignment.name)

    result = {
        "overdue": overdue,
        "due_soon": due_soon
    }

    print("Deadline check result:", result)

    return result
                
