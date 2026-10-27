from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from PyQt6.QtCore import QObject, pyqtSignal

from src.config.time import APP_TIMEZONE


class SchedulerSignals(QObject):

    job_completed = pyqtSignal(str, object)
    job_failed = pyqtSignal(str, str)


class AppScheduler:

    def __init__(self):

        self.signals = SchedulerSignals()

        self.scheduler = BackgroundScheduler(
            timezone=APP_TIMEZONE
        )

    def _execute_job(self, job_id, job_function):
        """Run a job and send its result back to UI"""

        try:
            result = job_function()
            self.signals.job_completed.emit(job_id, result)

        except Exception as exc: # noqa: BLE001

            self.signals.job_failed.emit(
                job_id,
                str(exc)
            )


    def add_interval_job(
        self,
        job_id,
        job_function,
        minutes = 0,
        hours = 0,
        run_immediately=False
    ):

        job_options = {
            "trigger": "interval",
            "minutes": minutes,
            "hours": hours, 
            "args": [job_id, job_function],
            "id": job_id,
            "replace_existing": True,
            "max_instances": 1,
            "coalesce": True,
        }

        if run_immediately:
            job_options["next_run_time"] = datetime.now(APP_TIMEZONE)
        
        self.scheduler.add_job(
            self._execute_job,
            **job_options
        )

    def add_daily_job(
        self,
        job_id,
        job_function,
        hour,
        minute=0,
        run_immediately=False
    ):
        self.scheduler.add_job(
            self._execute_job,
            trigger="cron",
            hour=hour,
            minute=minute,
            args=[job_id, job_function],
            id=job_id,
            replace_existing=True,
            max_instances=1,
            coalesce=True
        )

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)