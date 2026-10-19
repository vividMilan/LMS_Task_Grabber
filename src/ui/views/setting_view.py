import qtawesome as qta
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.services.credential_service import (
    delete_credentials,
    get_credentials,
    save_credentials,
)
from src.ui.components.toast_notification import ToastNotification
from src.ui.styles.tokens import COLORS


class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(20, 20, 20, 20)

        self.init_ui()

        self.update_theme_styles()

    def init_ui(self):

        self.setObjectName("settingsView")

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

        # Footer

        footer = QHBoxLayout()

        footer.addStretch()

        reset_button = QPushButton("Reset Button")
        reset_button.setObjectName("resetButton")

        save_button = QPushButton("Save Button")
        save_button.setObjectName("saveButton")


        footer.addWidget(reset_button)
        footer.addWidget(save_button)

        main_layout.addWidget(self.content_stack, stretch=1)
        root_layout.addLayout(main_layout, stretch=1)
        root_layout.addLayout(footer)

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
        navigation_frame = QFrame()
        navigation_frame.setObjectName("settingsNavigation")

        navigation_frame.setFixedWidth(200)

        layout = QVBoxLayout(navigation_frame)
        layout.setContentsMargins(12, 18, 12, 12)
        layout.setSpacing(10)

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
        return navigation_frame

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

        self.username_input = QLineEdit()

        self.username_input.setPlaceholderText("Username")


        password_container = QWidget()

        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(0)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.password_eye_button = QPushButton()

        self.password_eye_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.password_eye_button.setIcon(
            qta.icon("fa5s.eye")
        )

        self.password_eye_button.setFixedSize(40, 40)

        self.password_eye_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }

            QPushButton:hover {
                background: rgba(255, 255, 255, 20);
                border-radius: 5px;
            }
        """)

        self.password_eye_button.clicked.connect(
            self.toggle_password_visibility
        )

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.password_eye_button)

        self.render_credentials()

        submit_btn = QPushButton("Save Credentials")
        delete_btn = QPushButton("Delete Credentials")


        submit_btn.clicked.connect(self.save_lms_credentials)
        delete_btn.clicked.connect(self.delete_credentials_btn)

        layout.addLayout(heading)

        layout.addWidget(self.username_input)
        layout.addWidget(password_container)
        layout.addWidget(submit_btn)
        layout.addWidget(delete_btn)

        layout.addStretch()
        return widget

    def toggle_password_visibility(self):

        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:

            self.password_input.setEchoMode(
                QLineEdit.EchoMode.Normal
            )

            self.password_eye_button.setIcon(
                qta.icon("fa5s.eye-slash")
            )
        else:

            self.password_input.setEchoMode(
                QLineEdit.EchoMode.Password
            )

            self.password_eye_button.setIcon(
                qta.icon("fa5s.eye")
            )


    def delete_credentials_btn(self):
            delete_credentials()
            self.render_credentials()
            ToastNotification(self, text="Credential Deleted Successfully", bg_color=COLORS.success.name())

    def render_credentials(self):

        username, password = get_credentials()

        if username:
            self.username_input.setText(username)

        if password:
            self.password_input.setText(password)

    def save_lms_credentials(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()


        if not username or password:
            pass

        existing_username, existing_password = get_credentials()

        if username == existing_username and password == existing_password:
            ToastNotification(self, text="Credentials Already Saved", bg_color=COLORS.warning.name(), duration=3000)
            return

        save_credentials(username=username, password=password)
        self.render_credentials()

        ToastNotification(self, text="Credentials Saved", bg_color=COLORS.success.name(), duration=3000)

        print("Credentials saved")

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

        notification_layout, self.notification_combo = self._create_combo_box("Start reminding me before ", ["3 Day", "5 Days", "1 Week", "2 Week", "1 Month"])

        layout.addLayout(notification_layout)
        
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

        theme_layout, self.theme_combo = self._create_combo_box("Theme Preference", ["Dark Mode", "Light Mode"])

        accent_combo_layout, self.accent_combo = self._create_combo_box("Accent Color", ["Orange", "Green", "Indigo", "Blue"])

        layout.addLayout(heading)
        layout.addLayout(theme_layout)
        layout.addLayout(accent_combo_layout)

        layout.addStretch()
        return widget

    def _create_card(self, title: str, description: str):

        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setContentsMargins(0, 0, 0, 0)
        title_label.setObjectName("cardTitle")

        description_label = QLabel(description)
        description_label.setContentsMargins(0, 0, 0, 0)
        description_label.setObjectName("cardDescription")

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.setSpacing(4)


        return layout

    def _create_combo_box(self, label: str, options: list):
        input_layout = QVBoxLayout()
        
        input_label = QLabel(label)
        input_label.setObjectName("inputLabel")
        
        input_widget = QComboBox()

        input_widget.addItems(options)
        
        input_layout.addWidget(input_label)
        input_layout.addWidget(input_widget)
        input_layout.setSpacing(4)

        return input_layout, input_widget

    def _create_checkbox(self, label: str):
        return QCheckBox(label)

    def _on_theme_preference_changed(self, selected_mode: str):
        pass
    
    def update_theme_styles(self):

        self.setStyleSheet(f"""

            QWidget#settingsView {{
                background-color: {COLORS.window_bg.name()};
                color: {COLORS.text_primary.name()};

            }}

            #settingsNavigation {{
                background-color: {COLORS.card_bg.name()};
                border: 1px solid {COLORS.border.name()};
                border-radius: 12px;
            }}

            QLabel#settingsHeader {{
                color: {COLORS.text_primary.name()};
                font-size: 25px;
                font-weight: bold;
            }}

            QLabel#settingsSubheader {{
                font-size: 14px;
                color: {COLORS.text_secondary.name()};
            }}


            QListWidget#settingsList {{
                background: transparent;
                border: none;
                outline: none;
            }}

            QListWidget#settingsList::item {{
                background: transparent;
                color: {COLORS.text_secondary.name()};
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }}

            QListWidget#settingsList::item:hover {{
                background: {COLORS.text_primary.name()};
                color: {COLORS.accent.name()};
            }}

            QListWidget#settingsList::item:selected {{
                background: {COLORS.accent_light.name()};
                color: {COLORS.accent.name()};
            }}

            QPushButton#resetButton {{
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 8px;
                background-color: {COLORS.text_secondary.name()};
                color: {COLORS.window_bg.name()};
                border: 1px solid {COLORS.border.name()};
            }}

            QPushButton#saveButton {{            
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 8px;
                background-color: {COLORS.accent.name()};
                color: {COLORS.text_primary.name()};
            }}

            QPushButton#saveButton:hover {{
                background-color: {COLORS.accent_hover.name()};
            }}

            QLabel#cardTitle {{
                font-size: 18px;
                font-weight: bold;
                color: {COLORS.text_primary.name()};
            }}

            QLabel#cardDescription {{
                font-size: 12px;
                color: {COLORS.text_secondary.name()};
            }}

            QLabel#inputLabel {{
                color: {COLORS.text_primary.name()};
                font-size: 12px;
            }}

            QComboBox {{
                min-height: 34px;
                background-color: #F9FAFB;
                border: 1px solid {COLORS.border.name()};
                border-radius: 7px;
                padding: 0px 10px;
                color: black;
            }}

            QComboBox:hover {{
                border-color: {COLORS.accent_light.name()};
            }}

            QComboBox:focus {{
                border-color: {COLORS.accent.name()};
            }}

            QComboBox:drop-down {{
                border: none;
                width: 28px;
            }}

            QCheckBox {{
                spacing: 8px;
                color: {COLORS.text_primary.name()};
                font-size: 12px;
            }}

            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 1px solid {COLORS.border.name()};
                border-radius: 5px;
                background-color: {COLORS.card_bg.name()};
            }}

            QCheckBox::indicator:checked {{
                background-color: {COLORS.accent.name()};
                border-color: {COLORS.accent_light.name()};
            }}

        """)