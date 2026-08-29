
import sys
from pathlib import Path

from PyQt6.QtCore import QFileSystemWatcher
from PyQt6.QtWidgets import QApplication

from src.database.connection import init_db
from src.ui.main_window import MainWindow

init_db()

def cli_mode():
    """Runs the script in CLI mode."""
    print("Running in CLI mode...")

class QSSWatcher:
    def __init__(self, app: QApplication, qss_relative_path: str):
        self.app = app
        self.qss_path = Path(__file__).resolve().parent / qss_relative_path
        
        self.watcher = QFileSystemWatcher([str(self.qss_path)])
        self.watcher.fileChanged.connect(self.reload_styles)
        
        self.reload_styles()

    def reload_styles(self):
        if self.qss_path.exists():
            with open(self.qss_path, "r", encoding="utf-8") as f:
                self.app.setStyleSheet(f.read())
            print("[QSS] Stylesheet reloaded.")

def gui_mode():
    app = QApplication(sys.argv)
    _qss_watcher = QSSWatcher(app, "ui/styles/style.qss")
    window = MainWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # cli_mode()
    gui_mode()
