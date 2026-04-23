from PyQt6.QtWidgets import QScrollArea, QFrame, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from ui.components.task_card import TaskCard
from ui.theme import Theme

class TaskList(QScrollArea):
    def __init__(self, tasks):
        super().__init__()

        self.tasks = tasks

        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(16)

        self.populate()
        self.setWidget(content)

    def refresh(self, new_tasks):
        self.tasks = new_tasks

        # remove task cards from list
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            card = item.widget()

            if card:
                card.deleteLater()

        # rebuild
        if not new_tasks:
            self.show_empty_state()

        else:
            for task in new_tasks:
                self.content_layout.addWidget(TaskCard(task))
        
        self.content_layout.addStretch()

    def populate(self):
        if not self.tasks:
            self.show_empty_state()
        else:
            for task in self.tasks:
                self.content_layout.addWidget(TaskCard(task))


    def show_empty_state(self):
        label = QLabel("No Upcoming Tasks Found")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(
            Theme.get_font(Theme.Fonts.MEDIUM, bold=True)
        )

        label.setStyleSheet(
            f"color: {Theme.Colors.TEXT_MUTED}"
        )

        self.content_layout.addWidget(label)