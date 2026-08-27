import re
from datetime import datetime
from zoneinfo import ZoneInfo

from src.utils.string_extractors import split_viva_times

LOCAL_TIMEZONE = ZoneInfo("Asia/Colombo")


def parse_due_date(input_due_text) -> datetime | None:

    try:
        removed_prefix = input_due_text.strip().split()[1:]

        due_text = " ".join(removed_prefix)

        return datetime.strptime(due_text, "%A, %d %B %Y, %I:%M %p").replace(
            tzinfo=LOCAL_TIMEZONE
        )
    except ValueError as e:
        print(f"[!] Error parsing due date: {e}")
        return None


def parse_viva_time(input_viva_times: str) -> tuple[datetime, datetime] | None:

    selection = split_viva_times(input_viva_times)

    # Pattern 1: "14.08.2026 (13.00 - 15.00 hrs)"
    match = re.search(
        r"(\d{2}.\d{2}.\d{4})\s*\((\d{2}.\d{2})\s*-\s*(\d{2}.\d{2})\s*hrs\)", selection
    )

    if match:
        date = match.group(1)  # 14.08.2026
        start_time = match.group(2)  # 13.00
        end_time = match.group(3)  # 15.00

        start_date_time = datetime.strptime(
            f"{date} {start_time}", "%d.%m.%Y %H.%M"
        ).replace(tzinfo=LOCAL_TIMEZONE)
        end_date_time = datetime.strptime(
            f"{date} {end_time}", "%d.%m.%Y %H.%M"
        ).replace(tzinfo=LOCAL_TIMEZONE)

        return start_date_time, end_date_time

    # Pattern 2: "2026-08-16 - 02.00 PM - 03.00 PM"
    match = re.search(
        r"(\d{4}.\d{2}.\d{2})\s*.\s*(\d{1,2}.\d{1,2})\s*([AaPp][Mm])\s*.\s*(\d{2}.\d{2})\s*([AaPp][Mm])",
        selection,
    )

    if match:
        date = match.group(1)  # 2026-08-16
        start_time = f"{match.group(2)} {match.group(3)}"  # 02:00 PM
        end_time = f"{match.group(4)} {match.group(5)}"  # 03:00 PM

        start_date_time = datetime.strptime(
            f"{date} {start_time}", "%Y-%m-%d %I:%M %p"
        ).replace(tzinfo=LOCAL_TIMEZONE)
        end_date_time = datetime.strptime(
            f"{date} {end_time}", "%Y-%m-%d %I:%M %p"
        ).replace(tzinfo=LOCAL_TIMEZONE)

        return start_date_time, end_date_time

    return None
