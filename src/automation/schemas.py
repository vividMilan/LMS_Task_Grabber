from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScrappedAssignment:
    course_id: str = ""
    course_name: str = ""
    heading: str = ""
    due_date: datetime | None = None
    link: str = ""
    file_path: str | None = None
    file_link: str | None = None
    type: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
