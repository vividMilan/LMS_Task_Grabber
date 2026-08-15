from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ScrappedAssignment:
    course_id: str = ""
    course_name: str = ""
    heading: str = ""
    due_date: Optional[datetime] = None
    link: str = ""
    file_path: Optional[str] = None
    file_link: Optional[str] = None
    type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None