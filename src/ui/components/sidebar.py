import qtawesome as qta
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout

from src.ui.styles.tokens import COLORS

INACTIVE_ICON_COLOR = "#ee5e0b"  # Default orange icon
ACTIVE_ICON_COLOR = "#ffffff" 
BUTTON_SIZE = 48
class Sidebar(QFrame):

    page_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._init_ui()

        self.apply_styles()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        home_icon = qta.icon(
            "ei.home",
            color=INACTIVE_ICON_COLOR,
            color_active=ACTIVE_ICON_COLOR,
            color_selected=ACTIVE_ICON_COLOR
        )

        calender_icon = qta.icon(
            "fa5s.calendar-alt",
            color=INACTIVE_ICON_COLOR,
            color_active=ACTIVE_ICON_COLOR,
            color_selected=ACTIVE_ICON_COLOR
        )

        tasks_icon = qta.icon(
            "ri.todo-fill", 
            color=INACTIVE_ICON_COLOR,
            color_active=ACTIVE_ICON_COLOR,
            color_selected=ACTIVE_ICON_COLOR
        )

        settings_icon = qta.icon(
            "ph.gear-fill",  
            color=INACTIVE_ICON_COLOR,
            color_active=ACTIVE_ICON_COLOR,
            color_selected=ACTIVE_ICON_COLOR
        )

        self.btn_dashboard = QPushButton(home_icon, "")
        self.btn_tasks = QPushButton(tasks_icon, "")
        self.btn_calender = QPushButton(calender_icon, "")
        self.btn_settings = QPushButton(settings_icon, "")

        self.buttons = [
            self.btn_dashboard,
            self.btn_tasks,
            self.btn_calender,
            self.btn_settings
        ]

        for index, btn in enumerate(self.buttons):
            btn.setCheckable(True)
            btn.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
            btn.setIconSize(QSize(24, 24))
            btn.clicked.connect(lambda _, idx=index: self.set_active_page(idx))
            layout.addWidget(btn)

        self.set_active_page(0)

    def set_active_page(self, index: int):
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)
        self.page_changed.emit(index)

    def apply_styles(self):
        self.setStyleSheet(f"""
            QFrame#sidebar {{
                background-color: {COLORS.dark_bg.name()};
                border-right: 1px solid {COLORS.border.name()};
                padding: 10px;
                min-width: 60px;
                max-width: 60px;
            }}

            /* Sidebar Icon Buttons */
            QFrame#sidebar QPushButton {{
                border: 2px solid {COLORS.accent.name()};
                border-radius: 8px;
                padding: 8px;
                background-color: {COLORS.accent_light.name()};
            }}

            /* Hover state: Light orange background */
            QFrame#sidebar QPushButton:hover {{
                background-color: {COLORS.accent_hover.name()};
            }}

            /* Checked state: Solid orange background (Icon turns white automatically) */
            QFrame#sidebar QPushButton:checked {{
                background-color: {COLORS.accent.name()};
            }}

            /* Hovering while checked */
            QFrame#sidebar QPushButton:checked:hover {{
                background-color: {COLORS.accent_hover.name()};
            }}

        """)