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
    QComboBox,
    QCheckBox
)


class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(20, 20, 20, 20)
        self.init_ui()

    def init_ui(self):

        self.setObjectName("settingsView")

        self.setStyleSheet("""
            QWidget#settingsView {
                background-color: #F54927;
                color: #1F2937;
                font-family: "Segoe UI";
            }

            QLabel#settingsHeader {
                font-size: 25px;
                font-weight: bold;
                color: #111827;
            }

            QLabel#settingsSubheader {
                font-size: 14px;
                color: #6B7280;
            }
        """)

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

        header.setObjectName("settingsHeader")
        subheader.setObjectName("settingsSubheader")
        
        header_layout.addWidget(header)
        header_layout.addWidget(subheader)

        return header_layout

    def _create_navigation_panel(self):
        frame = QFrame()
        frame.setObjectName("settingsNavigation")

        frame.setStyleSheet("""
                background-color: #F3F4F6;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
        """)

        frame.setFixedWidth(200)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 18, 12, 12)
        layout.setSpacing(10)

        self.settings_list = QListWidget()

        self.settings_list.setStyleSheet("""

            QListWidget {            
                background: transparent;
                border: none;
                outline: none;
            }

            QListWidget::item {
                background: transparent;
                color: #6b7280;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }

            QListWidget::item:hover {
                background: #FEEFE7;
                color: #ee5e0b;
            }

            QListWidget::item:selected {
                background: #FCD3BB;
                color: #ee5e0b;
            }


        """)

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

        heading = self._create_card(title="Genaral", description="You can set genaral settings")

        layout.addLayout(heading)

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

        heading = self._create_card("Notification", "Change notification settings")

        layout.addLayout(heading)

        notification_input = self._create_combo_box("Start reminding me before ", ["3 Day", "5 Days", "1 Week", "2 Week", "1 Month"])

        layout.addLayout(notification_input)
        
        layout.addStretch()
        return widget

    def _create_automation_settings(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        heading = self._create_card(title="Automation", description="Change scraping and automation preference")

        auto_sync = self._create_checkbox("Run scraping in startup")
        background = self._create_checkbox("Run scraping in intervals")
        minimized = self._create_checkbox("Open app minimized in startup")

        layout.addLayout(heading)
        layout.addWidget(auto_sync)
        layout.addWidget(background)
        layout.addWidget(minimized)

        layout.addStretch()
        return widget

    def _create_theme_settings(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        heading = self._create_card(title="Theme", description="Change how the app looks")

        theme_preference = self._create_combo_box("Theme Preference", ["Dark Mode", "Light Mode", "System Preference"])

        accent_color = self._create_combo_box("Accent Color", ["Orange", "Green", "Indigo", "Blue"])

        layout.addLayout(heading)

        layout.addLayout(theme_preference)
        layout.addLayout(accent_color)

        layout.addStretch()
        return widget

    def _create_card(self, title: str, description: str):

        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setContentsMargins(0, 0, 0, 0)
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #111827;
        """)

        description_label = QLabel(description)
        description_label.setContentsMargins(0, 0, 0, 0)
        description_label.setStyleSheet("""
            font-size: 12px;
            color: #6B7280;
        """)

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.setSpacing(4)


        return layout

    def _create_combo_box(self, label: str, options: list):
        input_layout = QVBoxLayout()
        
        input_label = QLabel(label)
        
        input_widget = QComboBox()
        input_widget.addItems(options)
        
        input_layout.addWidget(input_label)
        input_layout.addWidget(input_widget)
        input_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignLeft)
        input_layout.setSpacing(4)

        return input_layout


    def _create_checkbox(self, label: str):
        checkbox = QCheckBox(label)
        
        checkbox.setStyleSheet("""
            
            QCheckBox {
                spacing: 8px;
                color: #374151;
                font-size: 12px;            
            }
        
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
        
                border: 1px solid #D1D5DB;
        
                border-radius: 5px;
        
                background-color: #FFFFFF;
            
            }
        
            QCheckBox::indicator:checked {
                background-color: #ee5e0b;
                border-color: 
            }
            
        
        """)

        return checkbox