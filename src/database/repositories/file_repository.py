from sqlalchemy.orm import Session

from ..models import File
from .base_repository import BaseRepository


class FileRepository(BaseRepository[File]):
    def __init__(self):
        super().__init__(File)

    def add_if_not_exists(
        self,
        db: Session,
        course_id: str,
        file_path: str,
        file_link: str,
        assignment_id: str,
    ) -> File:
        """Inserts a downloaded file record if the link hasn't been saved yet."""

        existing = (
            db.query(File)
            .filter(File.file_link == file_link, File.course_id == course_id)
            .first()
        )

        if existing:
            return existing

        return self.create(
            db,
            course_id=course_id,
            file_path=file_path,
            file_link=file_link,
            assignment_id=assignment_id,
        )


file_repo = FileRepository()
