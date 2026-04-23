from PyQt6.QtWidgets import QCalendarWidget
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QRect


class TaskCalendar(QCalendarWidget):
    def __init__(self):
        super().__init__()

        self.task_dates = set()

    def set_task_dates(self, dates):
        self.task_dates = dates
        self.updateCells()

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)

        if date in self.task_dates:
            painter.save()

            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            painter.setBrush(QBrush(QColor("#4F8CFF")))
            painter.setPen(Qt.PenStyle.NoPen)

            pill_width = 18
            pill_height = 5

            x = rect.center().x() - pill_width // 2
            y = rect.bottom() - 10

            painter.drawRoundedRect(
                x, 
                y, 
                pill_width, 
                pill_height,
                3,
                3
            )

            painter.restore()