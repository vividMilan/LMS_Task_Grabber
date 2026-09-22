from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ScrapedFile:
    file_path: str | None = None
    file_link: str | None = None

@dataclass
class ScrappedAssignment:

    # course
    course_id: str = ""
    course_name: str = ""

    # task
    heading: str = ""
    description: str = ""
    due_date: datetime | None = None
    link: str = ""
    type: str | None = None

    # file
    files: list[ScrapedFile] = field(
        default_factory=list
    )

    # viva if there are any
    start_time: datetime | None = None
    end_time: datetime | None = None
