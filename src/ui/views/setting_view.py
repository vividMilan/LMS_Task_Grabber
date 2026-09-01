from PyQt6.QtWidgets import QVBoxLayout, QLabel, QWidget, QTabWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QSpinBox, QCheckBox, QComboBox

class SettingsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        # Heading Section
        heading_label = QLabel("Settings")
        heading_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(heading_label)

        tabs = QTabWidget()
        tabs.addTab(self._genaral_tab(), "General")
        tabs.addTab(self._automation_tab(), "Automation")
        tabs.addTab(self._theme_tab(), "Theme")

        layout.addWidget(tabs)

    def _genaral_tab(self):
        general_tab = QWidget()
        layout = QFormLayout(general_tab)
        layout.addRow("Username:", QLineEdit("Jobhn Doe"))
        layout.addRow("Email:", QLineEdit("vividmilan@gmial.com"))
        layout.addRow("Save Interval (minutes):", QSpinBox(minimum=1, maximum=60, value=5))

        return general_tab

    def _automation_tab(self):
        automation_tab = QWidget()
        layout = QFormLayout(automation_tab)
        layout.addRow("Background Automation:", QCheckBox())
        layout.addRow("Automation Interval (minutes):", QSpinBox(minimum=1, maximum=60, value=10))

        return automation_tab

    def _theme_tab(self):
        theme_tab = QWidget()
        layout = QFormLayout(theme_tab)

        theme_combo = QComboBox()
        theme_combo.addItems(["Dark", "Light"])
        layout.addRow("Theme Preference", theme_combo)

        accent_combo = QComboBox()
        accent_combo.addItems(["Blue", "Green", "Red", "Purple"])
        layout.addRow("Accent Color", accent_combo)

        fonts_combo = QComboBox()
        fonts_combo.addItems(["Arial", "Helvetica", "Times New Roman", "Courier New"])
        layout.addRow("Font Preference", fonts_combo)

        return theme_tab