from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LMS Tracker")
        self.setGeometry(100, 100, 400, 200)

        # Main layout container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.button = QPushButton("Click me")
        self.button.clicked.connect(self.handle_click)
        layout.addWidget(self.button)

    def handle_click(self):
        self.button.setText("Clicked")