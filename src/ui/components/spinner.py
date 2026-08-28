
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtCore import QRectF, QTimer, Qt
from PyQt6.QtWidgets import (
    QWidget,
)


class Spinner(QWidget):

    def __init__(self, parent = None, size: int = 36, color: str = "#2563eb", width: int = 3):
        super().__init__(parent)
        self.size = size
        self.color = QColor(color)
        self.pen_width = width
        self.angle = 0

        self.setFixedSize(self.size, self.size)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._rotate)

    def _rotate(self):
        self.angle = (self.angle + 12) % 360
        self.update()

    def start(self):
        self.show()
        self.timer.start(25)

    def stop(self):
        self.timer.stop()
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(self.color, self.pen_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        margin = self.pen_width / 2
        rect = QRectF(
            margin, margin, self.size - self.pen_width, self.size - self.pen_width
        )

        painter.drawArc(rect, -self.angle * 16, 100 * 16)