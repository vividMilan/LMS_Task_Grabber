import uuid

from sqlalchemy.orm import Session

from src.automation.schemas import ScrappedAssignment
from src.database.repositories import (
    assignment_repo,
    course_repo,
    file_repo,
    viva_slot_repo,
)


def process_and_save_scraped_assignment(
    db: Session, scraped_items: list[ScrappedAssignment]
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

            _assignment, is_created = assignment_repo.upsert_assignment(
                db=db,
                assignment_id=assignment_id,
                type=item.type,
                link=item.link,
                course_id=item.course_id,
                name=item.heading,
                due=item.due_date,
                files=item.files
            )

            if item.start_time and item.end_time:
                viva_slot_repo.upsert_viva_slot(
                    db=db,
                    start_time=item.start_time,
                    end_time=item.end_time,
                    assignment_id=assignment_id,
                )

                print("Created Viva Slot")

            if is_created:
                stats["created"] += 1
            else:
                stats["updated"] += 1

            if item.file_link or item.file_path:
                file_repo.add_if_not_exists(
                    db=db,
                    course_id=item.course_id,
                    file_path=item.file_path,
                    file_link=item.file_link,
                    assignment_id=assignment_id,
                )

            course_repo.upsert_course(
                db=db, course_id=item.course_id, name=item.course_name
            )

    except Exception:
        db.rollback()
        raise

    return stats
