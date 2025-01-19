# =================================================================================================================
# Feature: base_job
# Dev: anhvt9
# Start Date: 09/11/2023
# Maintain Date: 09/11/2023
# =================================================================================================================

"""
    Description
"""

# =================================================================================================================

import schedule
import threading

# Declare Element =================================================================================================

TIME_UNIT_SECONDS = "seconds"
TIME_UNIT_MINUTES = "minutes"
TIME_UNIT_HOURS = "hours"
TIME_UNIT_DAYS = "days"
TIME_UNIT_WEEKS = "weeks"

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================
class BaseJob(schedule.Scheduler):
    def __init__(self) -> None:
        """"""
        super(BaseJob, self).__init__()
        self.cease_continuous_run = None
        self.counter = 0

    def start(self):
        """"""
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    self.run_pending()

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        self.cease_continuous_run = cease_continuous_run

    
    def run_one_time(self):
        """"""
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    self.run_pending()
                    if self.counter == 1:
                        self.stop()

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        self.cease_continuous_run = cease_continuous_run


    def stop(self):
        """"""
        if self.cease_continuous_run:
            self.cease_continuous_run.set()