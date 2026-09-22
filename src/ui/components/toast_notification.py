from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

class ToastNotification(QWidget):
    def __init__(self, parent=None, text="Notification", duration=3000, bg_color="#0078D4"):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.SubWindow)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        layout = QHBoxLayout(self)
        label = QLabel(text)
        label.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: #FFFFFF;
                font-weight: bold;
                font-size: 13px;
                padding: 10px 16px;
                border-radius: 6px;
            }}
        """)
        layout.addWidget(label)

        # Drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        self.adjustSize()

        # Position bottom-right corner of parent window
        if parent:
            p_geom = parent.geometry()
            self.move(p_geom.width() - self.width() - 20, p_geom.height() - self.height() - 20)

        # Auto dismiss
        QTimer.singleShot(duration, self.close)
        self.show()