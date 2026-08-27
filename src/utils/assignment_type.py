from src.database.models import AssignmentType


def assignment_type(heading: str) -> AssignmentType | None:
    heading_lower = heading.lower()
    if "viva" in heading_lower or "slot" in heading_lower:
        return AssignmentType.VIVA_SLOT
    elif "tma" in heading_lower:
        return AssignmentType.TMA
    elif "quiz" in heading_lower:
        return AssignmentType.QUIZ
    elif "project" in heading_lower:
        return AssignmentType.MINI_PROJECT
    elif "exam" in heading_lower or "test" in heading_lower:
        return "exam"
    else:
        return None
