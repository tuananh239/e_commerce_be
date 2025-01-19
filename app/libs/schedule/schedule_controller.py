# =================================================================================================================
# Feature: schedule_controller
# Dev: anhvt9
# Start Date: 09/11/2023
# Maintain Date: 09/11/2023
# =================================================================================================================

"""
    Description
"""

# =================================================================================================================

from typing import List

from app.libs.pattern.creational.singleton import Singleton
from app.libs.schedule.base_job import BaseJob

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================
class ScheduleController(metaclass=Singleton):
    def __init__(self, jobs: List[BaseJob]) -> None:
        """"""
        self.jobs = jobs

    
    def start_all(self):
        for job in self.jobs:
            job.start()

    
    def stop_all(self):
        for job in self.jobs:
            job.stop()