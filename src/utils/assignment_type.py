def assignment_type(heading: str) -> str | None:
    heading_lower = heading.lower()
    if "viva" in heading_lower or "slot" in heading_lower:
        return "Viva Slot"
    elif "assignment" in heading_lower:
        return "Assignment"
    elif "quiz" in heading_lower:
        return "Quiz"
    elif "project" in heading_lower:
        return "Mini Project"
    elif "exam" in heading_lower or "test" in heading_lower:
        return "Exam"
    else:
        return None
