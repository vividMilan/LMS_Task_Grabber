from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(20, 20, 20, 20)
        self.init_ui()

    def init_ui(self):
        root_layout = QVBoxLayout(self)

        # Header
        root_layout.addLayout(self._create_header())

        # Main horizontal layout
        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)

        # Left Nav
        navigation_panel = self._create_navigation_panel()
        main_layout.addWidget(navigation_panel)

        # Right Content Stack
        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self._create_general_settings())
        self.content_stack.addWidget(self._create_appearance_settings())
        self.content_stack.addWidget(self._create_notifications_settings())
        self.content_stack.addWidget(self._create_automation_settings())
        self.content_stack.addWidget(self._create_theme_settings())

        main_layout.addWidget(self.content_stack, stretch=1)
        root_layout.addLayout(main_layout, stretch=1)

    def _create_header(self):
        header_layout = QVBoxLayout()
        header = QLabel("Settings")
        subheader = QLabel("Configure your application settings below.")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        subheader.setStyleSheet("font-size: 16px; color: gray;")
        header_layout.addWidget(header)
        header_layout.addWidget(subheader)
        return header_layout

    def _create_navigation_panel(self):
        frame = QFrame()
        frame.setObjectName("settingsNavigation")
        frame.setFixedWidth(200)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 18, 12, 12)
        layout.setSpacing(10)

        title = QLabel("Settings")
        layout.addWidget(title)

        self.settings_list = QListWidget()
        self.settings_list.setObjectName("settingsList")

        # Associate each item with the QStackedWidget page index
        items = [
            ("General", 0),
            ("Appearance", 1),
            ("Notifications", 2),
            ("Automation", 3),
            ("Theme", 4)
        ]

        for label, index in items:
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, index)
            self.settings_list.addItem(item)

        self.settings_list.setCurrentRow(0)
        self.settings_list.currentItemChanged.connect(self._navigation_changed)

        layout.addWidget(self.settings_list)
        return frame

    def _navigation_changed(self, current, previous):
        if not current:
            return
        index = current.data(Qt.ItemDataRole.UserRole)
        self.content_stack.setCurrentIndex(index)

    # Individual page builders
    def _create_general_settings(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("General Settings"))
        layout.addStretch()
        return widget

    def _create_appearance_settings(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Appearance Settings"))
        layout.addStretch()
        return widget

    def _create_notifications_settings(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Notifications Settings"))
        layout.addStretch()
        return widget

    def _create_automation_settings(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Automation Settings"))
        layout.addStretch()
        return widget

    def _create_theme_settings(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Theme Settings"))
        layout.addStretch()
        return widget