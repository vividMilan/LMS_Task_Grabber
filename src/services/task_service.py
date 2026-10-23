from sqlalchemy.exc import SQLAlchemyError

from src.database.connection import SessionLocal
from src.database.models import Assignment


class TaskService:

    @staticmethod
    def set_completed(task_id: str, is_completed: bool) -> bool:
        """Toggle completion of assignment"""

        db = SessionLocal()

        try:
            assignment = (
                db.query(Assignment).filter(Assignment.id == task_id).first()
            )

            if assignment is None:
                return False

            assignment.completed = is_completed
            db.commit()

            return True
            
            
        except SQLAlchemyError:
            db.rollback()
            raise
        finally:
            db.close()