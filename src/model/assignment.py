from datetime import datetime

class Assignment:
    def __init__(self, name, course, due_date, link):
        self.name = name
        self.course = course
        self.due_date = due_date
        self.link = link

    def print_info(self):

        days_left = (self.due_date - datetime.today())
        hours_left = days_left.seconds // 3600
        minutes_left = (days_left.seconds % 3600) // 60

        print("==============================================")
        print(f"Name        : {self.name}")
        print(f"Course      : {self.course}")
        print(f"Link        : {self.link}")
        print(f"Due Date    : {self.due_date.date()}")
        print(f"Due Time    : {self.due_date.time()}")
        print(f"Time Left   : {days_left.days} Days {hours_left} hrs {minutes_left} minutes left")
