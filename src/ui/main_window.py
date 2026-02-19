from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LMS Task Grabber")
        self.setMinimumSize(600, 400)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.on_click)

        layout.addWidget(self.button)
        central_widget.setLayout(layout)

    def on_click(self):
        print("Button clicked!")