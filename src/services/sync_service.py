from typing import List
from sqlalchemy.orm import Session
from src.database.repositories import assignment_repo, course_repo, file_repo
from src.automation.schemas import ScrappedAssignment
import uuid


def process_and_save_scraped_assignment(
    db: Session,
    scraped_items: List[ScrappedAssignment]
) -> dict:
    """Iterates through scraped assignments, ensures course records exist,

    and upserts assignments into the local database.
    """

    stats = {"created": 0, "updated": 0, "total": len(scraped_items)}

    try:
        for item in scraped_items:

            course_repo.upsert_course(
                db=db, course_id=item.course_id, name=item.course_name
            )

            assignment_id = str(uuid.uuid4())

            assignment, is_created = assignment_repo.upsert_assignment(
                db=db,
                assignment_id=assignment_id,
                type=item.type,
                link=item.link,
                course_id=item.course_id,
                name=item.heading,
                due=item.due_date,
            )

            if is_created:
                stats["created"] += 1
            else:
                stats["updated"] += 1

            if (item.file_link or item.file_path):
                file_repo.add_if_not_exists(db=db, course_id=item.course_id, file_path=item.file_path, file_link=item.file_link, assignment_id=assignment_id)

            course_repo.upsert_course(db=db, course_id=item.course_id, name=item.course_name)

            
    except Exception as e:
        db.rollback()
        stats["updated"]
        raise e

    return stats