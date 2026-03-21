import sqlite3
from tabulate import tabulate

DB_NAME = "assignments.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            courseCode TEXT NOT NULL,
            course TEXT NOT NULL,
            due_date TEXT NOT NULL,
            due_time TEXT NOT NULL,
            link TEXT NOT NULL,
            completed Boolean NOT NULL DEFAULT 0,
            FOREIGN KEY (courseCode) REFERENCES courses(code)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            excluded Boolean NOT NULL DEFAULT 0
        )
    ''')


    conn.commit()
    conn.close()

def save_assignment(assignment):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    course_exists = cursor.execute("SELECT 1 FROM courses WHERE code = ?", (assignment["courseCode"],)).fetchone()

    if not course_exists:
        cursor.execute("INSERT INTO courses (code, name) VALUES (?, ?)", (assignment["courseCode"], assignment["course"]))

    cursor.execute('''
        INSERT INTO assignments (name, course, courseCode, due_date, due_time, link, completed)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (assignment["name"], assignment["course"], assignment["courseCode"], assignment["due_date"].strftime("%Y-%m-%d"), assignment["due_date"].strftime("%H:%M"), assignment["link"], assignment.get("completed", 0)))
    conn.commit()
    conn.close()

def print_all_assignments():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Fetch all rows
    cursor.execute("SELECT * FROM assignments")
    rows = cursor.fetchall()
    
    if not rows:
        print("No assignments found in the database.")
        return
    
    # Define table headers
    headers = ["ID", "Name", "Course", "Course Code", "Due Date", "Due Time", "Link", "Completed"]
    
    # Print using tabulate
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    conn.close()


def print_all_courses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Fetch all rows
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()
    
    if not rows:
        print("No courses found in the database.")
        return
    
    # Define table headers
    headers = ["Course Code", "Course Name", "Excluded"]
    
    # Print using tabulate
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    conn.close()