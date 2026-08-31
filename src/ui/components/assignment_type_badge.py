from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

# Color mapping for assignment types
TYPE_COLORS = {
    "tma": "#FF5722",          # Vivid Orange (Warm Accent)
    "mini_project": "#6366F1", # Indigo / Violet (Cool Purple)
    "quiz": "#06B6D4",         # Electric Cyan (Light Bright Blue)
    "viva": "#10B981",         # Emerald Green (Fresh Green)
    "lab_report": "#EC4899",   # Vibrant Pink / Magenta (Warm Pink)
    "exam": "#EF4444",         # High-Alert Red (Critical Red)
}

class assignmentType(QWidget):
    def __init__(self, assignment_type: str, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._init_ui(assignment_type=assignment_type)

    def _init_ui(self, assignment_type: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Format label text (e.g., "mini_project" -> "MINI PROJECT")
        display_text = assignment_type.replace("_", " ").upper()
        type_text = QLabel(display_text)
        type_text.setObjectName("assignmentType")

        # Get background color based on type (defaults to orange)
        bg_color = TYPE_COLORS.get(assignment_type.lower(), "#EE5E0B")

        # Apply pill styling with internal padding and rounded corners
        type_text.setStyleSheet(f"""
            QLabel#assignmentType {{
                background-color: {bg_color};
                color: #FFFFFF;
                font-size: 11px;
                font-weight: bold;
                border-radius: 4px;
                padding: 3px 8px;
                margin: 0px;
            }}
        """)

        layout.addWidget(type_text)