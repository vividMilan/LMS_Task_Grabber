from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ScrappedAssignment:
    course_id: str
    course_name: str
    heading: str
    due_date: Optional[datetime]
    link: str
    file_path: Optional[str]
    file_link: Optional[str]
    type: Optional[str]