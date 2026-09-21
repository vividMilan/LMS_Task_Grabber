import hashlib

from sqlalchemy.orm import Session

from src.automation.schemas import ScrappedAssignment
from src.database.repositories import (
    assignment_repo,
    course_repo,
    file_repo,
    viva_slot_repo,
)


def generate_assignment_id(course_id: str, link: str):
    value = f"{course_id}:{link}"
    return hashlib.sha256(value.encode()).hexdigest()


def process_and_save_scraped_assignment(
    db: Session, scraped_items: list[ScrappedAssignment]
) -> dict:
    """Iterates through scraped assignments, ensures course records exist,

    and upserts assignments into the local database.
    """

    stats = {
        "created": 0, 
        "updated": 0, 
        "total": len(scraped_items)
    }

    try:
        for item in scraped_items:

            # ----------------- Ensure Code exits ---------------------
            course_repo.upsert_course(
                db=db, course_id=item.course_id, name=item.course_name
            )

            # ------------ Genarate assignment ID -----------------

            assignment_id = generate_assignment_id(
                course_id=item.course_id,
                link=item.link
            )

            # ------------ Save/Upadate Assignment

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

            # ---------------- Save Viva slot if exists ------------------------

            if item.start_time and item.end_time:
                viva_slot_repo.upsert_viva_slot(
                    db=db,
                    start_time=item.start_time,
                    end_time=item.end_time,
                    assignment_id=assignment_id,
                )

                print("Created Viva Slot")


            # --------------- Update Stats ----------------------

            if is_created:
                stats["created"] += 1
            else:
                stats["updated"] += 1

            # ----------------- Save assignment files --------------------

            for file in item.files:

                if file.file_link or file.file_path:
                    file_repo.add_if_not_exists(
                        db=db,
                        course_id=item.course_id,
                        file_path=file.file_path,
                        file_link=file.file_link,
                        assignment_id=assignment_id,
                    )

            course_repo.upsert_course(
                db=db, course_id=item.course_id, name=item.course_name
            )

    except Exception:
        db.rollback()
        raise

    return stats
