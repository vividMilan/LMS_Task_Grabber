from .assignment_repository import assignment_repo
from .course_repository import course_repo
from .file_repository import file_repo
from .viva_slot_repository import viva_slot_repo

__all__ = [
    "course_repo",
    "file_repo",
    "assignment_repo",
    "viva_slot_repo"
]