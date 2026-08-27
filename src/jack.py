import sqlite3
from pathlib import Path

# Build absolute path relative to this script: src/ -> parent directory (LMS_Task_Grabber) -> data/app.db
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "app.db"

# Ensure the parent directory ('data') exists before connecting
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    query = "SELECT link FROM assignments WHERE id = ?"
    target_id = "b5b40771-a49a-42f5-820a-f0dc5a86e414"

    rows = cursor.execute(query, (target_id,)).fetchall()

    for (link,) in rows:
        print(link)


# import re

# def split_viva_times(input: str) -> str:
#     return input.split(":", 1)[1].strip()

# # input_viva_times = "Your selection: 14.08.2026 (13.00 - 15.00 hrs)"


# # # input_viva_times4 = "Your selection: 30th July 2026 - 1PM to 4PM"

# # selection = split_viva_times(input=input_viva_times)

# # match = re.search(
# #     r"(\d{2}.\d{2}.\d{4})\s*\((\d{2}.\d{2})\s*-\s*(\d{2}.\d{2})\s*hrs\)",
# #     selection
# # )

# # print("======================================")
# # print(match.group(1))
# # print(f"{match.group(2)}")
# # print(f"{match.group(3)}")

# # input_viva_times2 = "Your selection: 2026-08-16 | 02:00 PM - 03:00 PM"

# # selection2 = split_viva_times(input=input_viva_times2)

# # match2 = re.search(
# #     r"(\d{4}.\d{2}.\d{2})\s*.\s*(\d{1,2}.\d{1,2})\s*([AaPp][Mm])\s*.\s*(\d{2}.\d{2})\s*([AaPp][Mm])",
# #     selection2
# # )
# # print("======================================")
# # print(match2.group(1))
# # print(f"{match2.group(2)} {match2.group(3)}")
# # print(f"{match2.group(4)} {match2.group(5)}")

# input_viva_times3 = "Your selection: 4th Aug 1.30pm - 3.30pm"

# selection3 = split_viva_times(input_viva_times3)

# match3 = re.search(
#     r"(\d{1})(?:th|st|nd|rd)\s*([A-Za-z]{3,9})\s*((\d{1,2}).(?:\d{2})?)\s*([AaPp][Mm])\s*.\s*((\d{1,2}).(?:\d{2})?)([AaPp][Mm])",
#     selection3
# )

# print("======================================")
# print(f"{match3.group(1)}-")
# print(match3.group(2))
# print(match3.group(4))
# print(match3.group(5))
# print(match3.group(6))

# # input_viva_times4 = "Your selection: 30th July 2026 - 1PM to 4PM"
# # selection4 = split_viva_times(input_viva_times4)

# # match4 = re.search(
# #     r"(\d{1,2})(?:th|nd|rd|st)\s*([A-Za-z]{3,9})\s*(\d{4})\s*.\s*((\d{1,2})(?::|\.)?(?:\d{2})?[AaPp][Mm])\s*(?:.{1,2})\s*((\d{1,2})(?::|\.)?(?:\d{2})?[AaPp][Mm])",
# #     selection4
# # )

# # print("======================================")
# # print(match4.group(1))
# # print(match4.group(2))
# # print(match4.group(3))
# # print(match4.group(4))
# # print(match4.group(5))
# # print(match4.group(6))
# # print(match4.group(7))
