from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from src.database.models import AssignmentType


@dataclass
class ScrapedFile:
    file_path: Optional[str] = None
    file_link: Optional[str] = None

@dataclass
class ScrappedAssignment:

    # course
    course_id: str = ""
    course_name: str = ""

    # task
    heading: str = ""
    due_date: Optional[datetime] = None
    link: str = ""
    type: Optional[str] = None

    # file
    files: List[ScrapedFile] = field(
        default_factory=list
    )

    # viva if there are any
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
