from PyQt6.QtCore import QEvent, QSettings, QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QMenu,
    QMessageBox,
    QStackedWidget,
    QSystemTrayIcon,
    QWidget,
)
from sqlalchemy.exc import SQLAlchemyError

from src.services.due_notification_service import check_deadlines
from src.services.sheduler_service import AppScheduler
from src.services.sync_service import sync_assignments
from src.services.task_service import TaskService
from src.ui.components.sidebar import Sidebar
from src.ui.components.spinner import Spinner
from src.ui.components.toast_notification import ToastNotification
from src.ui.styles.tokens import COLORS
from src.ui.views.assignment_view import AssignmentView
from src.ui.views.calander_view import CalendarView
from src.ui.views.dashboard_view import DashboardView
from src.ui.views.setting_view import SettingsView
from src.ui.views.tasks_view import TasksView


class ScrapperWorker(QThread):
    finished_signal = pyqtSignal(bool, str) # Emits success status and message

    def run(self):
        try:

            success, message = sync_assignments()
            self.finished_signal.emit(
                success, 
                message
            )

        except Exception as e: # noqa: BLE001
            self.finished_signal.emit(False, str(e))

class MainWindow(QMainWindow):

    def __init__(self):

        self.settings = QSettings("LMS Tracker", "LMS Tracker")

        super().__init__()

        self.setWindowTitle("LMS Tracker")
        self.setGeometry(100, 200, 1200, 700)
        self._init_ui()

        self.setup_tray()

        self.scheduler = AppScheduler()

        self.scheduler.signals.job_completed.connect(
            self.on_scheduled_job_completed
        )

        self.scheduler.signals.job_failed.connect(
            self.on_scheduled_job_failed
        )

        self.configure_interval_sync()

        self.scheduler.add_interval_job(
            job_id="deadline_check",
            job_function=check_deadlines,
            minutes=1
        )

        print("Starting LMS Tracker scheduler...")
        self.scheduler.start()
        print("Scheduler started:", self.scheduler.scheduler.running)

        QApplication.instance().aboutToQuit.connect(
            self.scheduler.stop
        )

        QTimer.singleShot(0, self.startup_sync_if_enabled)

    def should_start_minimized(self) -> bool:
        return self.settings.value(
            "automation/minimized",
            False,
            type=bool
        )

    def configure_interval_sync(self):
        enabled = self.settings.value(
            "automation/background",
            False,
            type=bool
        )

        if enabled:
            self.scheduler.add_daily_job(
                job_id="assignment_sync",
                job_function=sync_assignments,
                hour=12
            )

    def startup_sync_if_enabled(self):
        auto_sync = self.settings.value(
            "automation/auto_sync",
            False,
            type=bool
        )

        if auto_sync:
            self.start_sync_process()

    def _init_ui(self):

        # Central Root Widgets & Main horizontal Layout
        self.root_widget = QWidget()
        self.setCentralWidget(self.root_widget)
        main_layout = QHBoxLayout(self.root_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.spinner = Spinner()

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.switch_page)

        # Main area (stacked widget)
        self.content_stack = QStackedWidget()

        self.page_dashboard = DashboardView()


        # ======================
        # PAGES
        # ======================
        self.page_tasks = TasksView()
        self.page_assignment_view = AssignmentView()
        self.page_calender = CalendarView()
        self.page_settings = SettingsView()

        # ===================================
        # Signals
        # ====================================

        self.page_tasks.sync_requested.connect(
            self.start_sync_process
        )

        # =======================
        # Assignment Navigation
        # =======================

        self.page_tasks.assignment_clicked.connect(
            self.open_assignment
        )

        self.page_assignment_view.back_requested.connect(
            self.show_tasks
        )

        self.page_calender.assignment_clicked.connect(
            self.open_assignment
        )

        # add to the stack
        self.content_stack.addWidget(self.page_dashboard)
        self.content_stack.addWidget(self.page_tasks)
        self.content_stack.addWidget(self.page_calender)
        self.content_stack.addWidget(self.page_settings)
        self.content_stack.addWidget(self.page_assignment_view)

        # add to main layout & apply styles
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_stack)

        self.apply_styles()

        self.page_dashboard.completed_changed.connect(
            self.update_assignment_completion
        )

        self.page_tasks.completed_changed.connect(
            self.update_assignment_completion
        )

        self.page_calender.completed_changed.connect(
            self.update_assignment_completion
        )

        self.page_settings.settings_saved.connect(
            self.refresh_all_views
        )

    def changeEvent(self, event):
        if (
            event.type() == QEvent.Type.WindowStateChange
            and self.isMinimized()
        ):
            self.hide()

        super().changeEvent(event)

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)

        self.tray_icon.setIcon(
            self.windowIcon()
        )

        self.tray_icon.setToolTip('LMS tracker')

        tray_menu = QMenu()

        open_action = tray_menu.addAction("Open LMS Tracker")
        open_action.triggered.connect(self.show_window)

        sync_action = tray_menu.addAction("Sync Assignments")
        sync_action.triggered.connect(self.start_sync_process)

        tray_menu.addSeparator()


        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(
            QApplication.instance().quit
        )

        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.activated.connect(
            self.on_tray_activated
        )

        self.tray_icon.show()

    def show_window(self):
        self.showNormal()
        self.show()
        self.raise_()
        self.activateWindow()


    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()


    def closeEvent(self, event):
        # Hide instead of closing the application
        event.ignore()
        self.hide()

        self.tray_icon.showMessage(
            "LMS Tracker",
            "The app is still running in the system tray.",
            QSystemTrayIcon.MessageIcon.Information,
            3000,
        )

    def check_deadline_notification(self, deadlines=None):

        if deadlines is None:
            deadlines = check_deadlines()


        overdue = deadlines.get("overdue", [])
        due_soon = deadlines.get("due_soon", [])

        if not overdue and not due_soon:
            print("No upcoming deadline notifications.")
            return

        messages = []

        if overdue:
            messages.append(
                f"Overdue ({len(overdue)}): "
                + ", ".join(overdue[:3])
            )

        if due_soon:
            messages.append(
                f"Due within 24 hours ({len(due_soon)})"
                + ", ".join(overdue[:3])
            )

        message = "\n".join(messages)

        self.tray_icon.showMessage(
            "LMS Tracker - Deadline Reminder",
            message,
            QSystemTrayIcon.MessageIcon.Warning,
            1000
        )
        
    def start_sync_process(self):

        if hasattr(self, "worker") and self.worker.isRunning():
            return

        print("Strating Sync.....")

        self.page_tasks.set_syncing(True)

        self.worker = ScrapperWorker()
        self.worker.finished_signal.connect(self.on_sync_finished)
        self.worker.start()

    def on_sync_finished(self, success: bool, message: str):

        self.page_tasks.set_syncing(False)

        if not success:
            msg = QMessageBox(self)
            msg.setWindowTitle("Sync Failed")
            msg.setText(message)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
            return
        
        
        ToastNotification(
            parent=self, 
            text="Task successfully synced!", 
            bg_color=COLORS.success.name()
        )

        self.refresh_assignment_views()

    def open_assignment(self, task):
        print(
            "Opening assignment:",
            task.title
        )

        # Give the selected taskCard to AssingmentView
        self.page_assignment_view.set_assignment(
            task
        )

        # Switch Page
        self.content_stack.setCurrentWidget(
            self.page_assignment_view
        )

    def switch_page(self, index: int):
        self.content_stack.setCurrentIndex(
            index
        )

    def show_tasks(self):
        self.content_stack.setCurrentWidget(
            self.page_tasks
        )

    def apply_styles(self):
        self.root_widget.setObjectName("centralWidget")
        self.root_widget.setStyleSheet(f"""
            QWidget#centralWidget {{
                background-color: {COLORS.window_bg.name()};
                color: {COLORS.text_primary.name()};
            }}
        """)

    def on_scheduled_job_completed(self, job_id, result):
        """Handle scheduler results on the GUI Thread"""


        if job_id == "deadline_check":

            self.check_deadline_notification(result)


        elif job_id == "assignment_sync":

            success, message = result

            self.tray_icon.showMessage(
                "LMS Tracker - Automatic Sync",
                message,
                (
                    QSystemTrayIcon.MessageIcon.Information
                    if success
                    else QSystemTrayIcon.MessageIcon.Warning
                ),
                5000
            )

            if success:
                self.page_tasks.refresh_tasks()

            self.refresh_all_views()

    def on_scheduled_job_failed(self, job_id, error_message):
        self.tray_icon.showMessage(
            "LMS Tracker - Scheduler Error",
            f"{job_id}: {error_message}",
            QSystemTrayIcon.MessageIcon.Warning,
            5000,
        )


    def update_assignment_completion(
        self,
        task_id: str,
        is_completed: bool
    ) -> None:
        try:
            updated = TaskService.set_completed(
                task_id=task_id,
                is_completed=is_completed
            )

            if updated:
                self.refresh_all_views()

        except SQLAlchemyError as e:
            print(f"Error updating task completion: {e}")


    def refresh_assignment_views(self):
        """Refresh all view that display assignments"""
        self.page_tasks.refresh_tasks()

        self.page_calender.refresh_deadline_indicators()
        self.page_calender.refresh_calendar()

    def refresh_all_views(self):
        self.page_dashboard.refresh_dashboard()
        self.page_tasks.load_assingments()
