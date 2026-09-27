from dataclasses import dataclass, field
from datetime import datetime

from src.domain.enums.assignment_types import AssignmentType
from src.domain.types.file import FileData
from src.domain.types.course import CourseData

@dataclass
class AssignmentData:
    id: str
    name: str
    description: str | None
    course_id: str
    course: CourseData
    completed: bool
    type: AssignmentType | None
    due: datetime
    link: str

    files: list[FileData] = field(
        default_factory=list
    )