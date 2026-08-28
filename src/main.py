
import sys

from PyQt6.QtWidgets import QApplication

from src.database.connection import init_db
from src.ui.main_window import MainWindow

init_db()

def cli_mode():
    """Runs the script in CLI mode."""
    print("Running in CLI mode...")



def gui_mode():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # cli_mode()
    gui_mode()
