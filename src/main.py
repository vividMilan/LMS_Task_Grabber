
import sys

from PyQt6.QtCore import QFileSystemWatcher
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from src.config.resource_path import resource_path
from src.database.connection import init_db
from src.ui.main_window import MainWindow

init_db()

class QSSWatcher:
    def __init__(self, app: QApplication):
        self.app = app
        self.qss_path = resource_path("src/ui/styles/style.qss")

        if not self.qss_path.exists():
            raise FileNotFoundError(
                f"Stylesheet not found: {self.qss_path}"
            )
                
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
    app.setQuitOnLastWindowClosed(False)

    icon_path = resource_path("assets/logo.png")

    app.setWindowIcon(QIcon(str(icon_path)))
    _qss_watcher = QSSWatcher(app)
    
    window = MainWindow()

    if window.should_start_minimized():
        window.showMinimized()
    else:
        window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    # cli_mode()
    gui_mode()
