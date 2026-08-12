from datetime import datetime
from zoneinfo import ZoneInfo


def parse_due_date(due_text):
    try:
        removed_prefix = due_text.split(":")
        due_text = " ".join(removed_prefix)

        return datetime.strptime(
            due_text,
            "%A, %d %B %Y, %I:%M %p"
        ).replace(tzinfo=ZoneInfo("Asia/Colombo"))

    except ValueError as e:
        print(f"[!] Error parsing due date: {e}")
        return None