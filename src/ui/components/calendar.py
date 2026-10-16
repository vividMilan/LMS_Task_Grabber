from PyQt6.QtWidgets import QCalendarWidget, QHeaderView
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QPainter, QColor

from src.domain.types.assignment import AssignmentData
from src.ui.styles.tokens import COLORS, FONT_SIZES


class Calendar(QCalendarWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.assignment_dates = set()
        
        self.setObjectName("calendar")

        self.set_style_sheet()


    def set_assignment_dates(self, assignmnets: list[AssignmentData]):
        
        self.assignment_dates.clear()

        for assignment in assignmnets:
            if not assignment.due:
                continue

            due_date = assignment.due

            qdate = QDate(
                due_date.year,
                due_date.month,
                due_date.day
            )

            self.assignment_dates.add(qdate)

        self.update()

    def paintCell(self, painter: QPainter, rect, date):

        painter.save()


        if date.month() != self.monthShown():

            painter.setPen(
                QColor("#8b8b8b")
            )

        else:

            painter.setPen(
                COLORS.text_primary
            )

        painter.drawText(
            rect,
            Qt.AlignmentFlag.AlignCenter,
            str(date.day())
        )

        # Let QCalendarWidget draw the normal date 

        # Is there an assignment on this date ?
        if date in self.assignment_dates:

            #Dot Size
            dot_size = 6

            # center the dot 

            x = rect.center().x() - dot_size // 2

            y = rect.bottom() - 7

            painter.setBrush(COLORS.success)

            painter.setPen(Qt.PenStyle.NoPen)

            painter.drawEllipse(
                x,
                y,
                dot_size,
                dot_size
            )

        painter.restore()

    def set_style_sheet(self):
        self.setStyleSheet(f"""
            /* Base widget background */
            QCalendarWidget {{
                background-color: {COLORS.dark_bg.name()};
            }}

            /* Weekday header bar (Mon, Tue, Wed...) */
            #calendar QCalendarWidget QHeaderView::section,
            #calendar QHeaderView::section {{
                background-color: {COLORS.dark_bg.name()};
                color: {COLORS.text_secondary.name()};
                padding: 4px;
                border: none;
                font-size: {FONT_SIZES.sm}px;
                font-weight: bold;
            }}

            /* Navigation bar background at the top */
            #calendar QWidget#qt_calendar_navigationbar {{
                background-color: {COLORS.dark_bg.name()};
            }}

            /* Month/Year selection buttons and arrows */
            #calendar QToolButton {{
                color: {COLORS.text_primary.name()};
                background-color: transparent;
                icon-size: 20px;
                border: none;
                font-size: {FONT_SIZES.sm}px;
            }}

            #calendar QToolButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }}

            /* Calendar grid area */
            #calendar QAbstractItemView {{
                background-color: {COLORS.dark_bg.name()};
                color: {COLORS.text_primary.name()};
                selection-background-color: {COLORS.accent.name()};
                selection-color: #ffffff;
                border: none;
                outline: none;
                font-size: {FONT_SIZES.sm}px;
            }}
        """)
