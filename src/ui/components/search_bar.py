from  PyQt6.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel

class SearchBar(QWidget):
    def __init__(self, placeholder: str = "Search...", parent=None):
        super().__init__(parent)
        self.setObjectName("searchBar")
        self._init_ui(placeholder)


    def _init_ui(self, placeholder: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(6)

        # Embed Search Icon

        self.icon_label = QLabel()
        layout.addWidget(self.icon_label)


        # Line Input
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(placeholder)
        layout.addWidget(self.input_field)