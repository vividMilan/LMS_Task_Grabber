from src.database.models import AssignmentType


def assignment_type(heading: str) -> AssignmentType | None:
    heading_lower = heading.lower()
    if "viva" in heading_lower or "slot" in heading_lower:
        return AssignmentType.VIVA_SLOT
    if "lab" in heading_lower:
        return AssignmentType.LAB
    if "practical" in heading_lower:
        return AssignmentType.PRACTICAL
    elif "tma" in heading_lower:
        return AssignmentType.TMA
    elif "quiz" in heading_lower:
        return AssignmentType.QUIZ
    elif "project" in heading_lower:
        return AssignmentType.MINI_PROJECT
    elif "exam" in heading_lower:
        return AssignmentType.EXAM
    else:
        return None
