import qtawesome as qta
from PyQt6.QtCore import QEvent, QSettings, Qt, pyqtSignal
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

from src.config.time import get_due_soon_days, set_due_soon_days
from src.services.credential_service import (
    delete_credentials,
    get_credentials,
    save_credentials,
)
from src.ui.components.toast_notification import ToastNotification
from src.ui.styles.tokens import COLORS


class SettingsView(QWidget):

    settings_saved = pyqtSignal()

    def __init__(self, parent=None):
        self.settings = QSettings("LMS Tracker", "LMS Tracker")
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
        self.content_stack.addWidget(self._create_notifications_settings())
        self.content_stack.addWidget(self._create_automation_settings())

        # Footer

        footer = QHBoxLayout()

        footer.addStretch()

        reset_button = QPushButton("Reset Button")
        reset_button.setObjectName("resetButton")

        self.save_button = QPushButton("Save Button")
        self.save_button.setObjectName("saveButton")

        self.save_button.clicked.connect(
            self.save_settings
        )


        footer.addWidget(reset_button)
        footer.addWidget(self.save_button)

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
            ("Notifications", 1),
            ("Automation", 2),
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
        self.username_input.setObjectName("username")

        password_container = QWidget()
        password_container.setObjectName("passwordContainer")

        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(0)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setObjectName("password")

        self.password_input.installEventFilter(self)  

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.password_eye_button = QPushButton()

        self.password_eye_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.password_eye_button.setIcon(
            qta.icon(
                "fa5s.eye",
                color=COLORS.text_secondary.name()
            )
        )

        self.password_eye_button.setObjectName("passwordEyeButton")

        self.password_eye_button.setFixedSize(34, 34)
        self.password_eye_button.setToolTip(
            "Show password"
        )

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

    def eventFilter(self, watched, event):
        """
        Update the password container border when the password input gains or loses focus   
        """
        if watched is getattr(self, "password_input", None):
            if event.type() == QEvent.Type.FocusIn:
                self._set_password_container_focus(True)

            elif event.type() == QEvent.Type.FocusOut:
                self._set_password_container_focus(False)

        return super().eventFilter(watched, event)

    def _set_password_container_focus(self, focused: bool):
        container = self.findChild(
            QWidget,
            "passwordContainer"
        )

        if container is None:
            return

        container.setProperty("focused", focused)

        # Re-apply the stylesheet selector after the property changes
        container.style().unpolish(container)
        container.style().polish(container)
        container.update()
        
    def toggle_password_visibility(self):

        if self.password_input.echoMode() == QLineEdit.EchoMode.Password:

            self.password_input.setEchoMode(
                QLineEdit.EchoMode.Normal
            )

            self.password_eye_button.setIcon(
                qta.icon(
                    "fa5s.eye-slash",
                    color=COLORS.text_secondary.name()
                )
                
            )
        else:

            self.password_input.setEchoMode(
                QLineEdit.EchoMode.Password
            )

            self.password_eye_button.setIcon(
                qta.icon(
                    "fa5s.eye",
                    color=COLORS.text_secondary.name()
                )
            )

    def save_settings(self):
        due_soon_days = self.notification_combo.currentData()

        if due_soon_days is None:
            ToastNotification(
                self,
                text="Please selecte a reminder period",
                bg_color=COLORS.warning.name(),
                duration=3000
            )

            return

        try: 
            set_due_soon_days(int(due_soon_days))
        except ValueError as e:
            ToastNotification(
                self,
                text=str(e),
                bg_color=COLORS.warning.name(),
                duration=3000
            )

            return

        ToastNotification(
            self,
            text=f"Reminder period saved as {due_soon_days} days",
            bg_color=COLORS.success.name(),
            duration=3000
        )

        self.settings_saved.emit()



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

        notification_layout, self.notification_combo = self._create_combo_box("Start reminding me before ", [])

        options = [
            ("3 Days", 3),
            ("5 Days", 5),
            ("1 Week", 7),
            ("2 Weeks", 14),
            ("1 Month", 30)
        ]

        for label, days in options:
            self.notification_combo.addItem(label, days)

        saved_days = get_due_soon_days()
        index = self.notification_combo.findData(saved_days)

        if index >= 0:
            self.notification_combo.setCurrentIndex(index)

        else:
            self.notification_combo.setCurrentIndex(
                self.notification_combo.findData(7)
            )

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

        settings_value = self.settings.value(
                        "automation/auto_sync",
                        False,
                        type=bool
                    )

        background_value = self.settings.value(
            "automation/background",
            False,
            type=bool
        )

        minimized_value = self.settings.value(
            "automation/minimized",
            False,
            type=bool
        )

        auto_sync.setChecked(
            settings_value
        )

        background.setChecked(
            background_value
        )

        minimized.setChecked(
            minimized_value
        )
        
        auto_sync.toggled.connect(
            lambda checked: self.settings.setValue(
                "automation/auto_sync",
                checked
            )
        )

        background.toggled.connect(
            lambda checked: self.settings.setValue(
                "automation/background",
                checked
            )
        )

        minimized.toggled.connect(
            lambda checked: self.settings.setValue(
                "automation/minimized",
                checked
            )
        )

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

            /* Username input */
            QLineEdit#username {{
                min-height: 38px;
                background-color: {COLORS.card_bg.name()};
                border: 1px solid {COLORS.border.name()};
                border-radius: 8px;
                padding: 0px 12px;
                color: {COLORS.text_primary.name()};
                selection-background-color: {COLORS.accent.name()};
            }}

            QLineEdit#username:hover {{
                border-color: {COLORS.accent_light.name()};
            }}

            QLineEdit#username:focus {{
                border: 1px solid {COLORS.accent.name()};
            }}

            /* Unified password input container */
            QWidget#passwordContainer {{
                background-color: {COLORS.card_bg.name()};
                border: 1px solid {COLORS.border.name()};
                border-radius: 8px;
            }}

            QWidget#passwordContainer[focused="true"] {{
                border: 1px solid {COLORS.accent.name()};
            }}

            QLineEdit#password {{
                min-height: 38px;
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 0px 12px;
                color: {COLORS.text_primary.name()};
                selection-background-color: {COLORS.accent.name()};
            }}

            QPushButton#passwordEyeButton {{
                border: none;
                background: transparent;
                border-radius: 6px;
                padding: 4px;
            }}

            QPushButton#passwordEyeButton:hover {{
                background-color: {COLORS.window_bg.name()};
            }}

            QPushButton#passwordEyeButton:pressed {{
                background-color: {COLORS.border.name()};
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