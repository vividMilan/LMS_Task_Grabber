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