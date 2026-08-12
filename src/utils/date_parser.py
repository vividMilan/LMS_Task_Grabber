from datetime import datetime

def parse_due_date(input_due_text) -> datetime | None:

    try:
        removed_prefix = input_due_text.strip().split()[1:]

        due_text = " ".join(removed_prefix)
        
        return datetime.strptime(due_text, "%A, %d %B %Y, %I:%M %p")
    except Exception as e:
        print(f"[!] Error parsing due date: {e}")
        return None