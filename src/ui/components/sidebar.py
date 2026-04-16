from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import QSize, Qt
import qtawesome as qta
from ..theme import Theme


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(70)
        self.setObjectName("sidebar")
        self.setStyleSheet(self.get_styles())

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(10, 20, 10, 20)

        self.active_button = None

        # Buttons
        self.home_button = self._create_nav_button('fa5s.home')
        self.calendar_button = self._create_nav_button('fa5s.calendar-alt')
        self.settings_button = self._create_nav_button('fa5s.cog')

        self.layout.addWidget(self.home_button)
        self.layout.addWidget(self.calendar_button)
        self.layout.addWidget(self.settings_button)

        self.set_active_button(self.home_button)

    def _create_nav_button(self, icon_name):
        btn = QPushButton()
        btn.setObjectName("navButton")
        btn.setFixedSize(45, 45)
        btn.setIconSize(QSize(20, 20))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFont(Theme.get_font(Theme.Fonts.NORMAL))

        default_icon = qta.icon(icon_name, color=Theme.Colors.PRIMARY)
        hover_icon = qta.icon(icon_name, color=Theme.Colors.BG_WHITE)
        active_icon = hover_icon

        btn.setIcon(default_icon)
        btn.default_icon = default_icon
        btn.hover_icon = hover_icon
        btn.active_icon = active_icon
        btn.setProperty("active", False)

        def enterEvent(event):
            if not btn.property("active"):
                btn.setIcon(hover_icon)

        def leaveEvent(event):
            if not btn.property("active"):
                btn.setIcon(default_icon)

        btn.enterEvent = enterEvent
        btn.leaveEvent = leaveEvent
        btn.clicked.connect(lambda: self.set_active_button(btn))

        return btn

    def set_active_button(self, btn):
        if self.active_button is btn:
            return

        if self.active_button:
            self.active_button.setProperty("active", False)
            self.active_button.setIcon(self.active_button.default_icon)
            self.active_button.style().unpolish(self.active_button)
            self.active_button.style().polish(self.active_button)

        self.active_button = btn
        btn.setProperty("active", True)
        btn.setIcon(btn.active_icon)
        btn.style().unpolish(btn)
        btn.style().polish(btn)


    def get_styles(self):
        return f"""
        QWidget#sidebar {{
            background-color: {Theme.Colors.BG_WHITE};
            border-right: 1px solid {Theme.Colors.SIDEBAR_BG};
        }}

        QPushButton#navButton {{
            background-color: {Theme.Colors.SIDEBAR_BG};
            border: 5px solid {Theme.Colors.PRIMARY};
            border-radius: 12px;
        }}

        QPushButton#navButton:hover, QPushButton#navButton[active="true"] {{
            background-color: {Theme.Colors.PRIMARY};
        }}
        """