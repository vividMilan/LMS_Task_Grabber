from datetime import datetime

def strip_due(due: datetime) -> tuple[str, str]:
    due_date = due.strftime("%d %b %Y")
    due_time = due.strftime("%I:%M %p")

    return due_date, due_time