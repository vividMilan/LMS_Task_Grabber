from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

class assignmentType(QWidget):
    def __init__(self, assignmet_type: str,  parent = None):
        super().__init__(parent)

        self._init_ui(assignment_type=assignmet_type)


    def _init_ui(
        self,
        assignment_type: str
    ):
        layout = QHBoxLayout(self)

        type_text = QLabel(assignment_type)

        type_text.setObjectName("assignmentType")

        layout.addWidget(type_text)