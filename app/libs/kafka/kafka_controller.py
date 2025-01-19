# =================================================================================================================
# Feature: base_controller
# Dev: anhvt9
# Start Date: 18/10/2023
# Maintain Date: 18/10/2023
# =================================================================================================================

"""
    Description
"""

# =================================================================================================================
from typing import List
from app.libs.kafka.base_consumer import BaseComsumer
from app.libs.pattern.creational.singleton import Singleton

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================

class KafkaController(metaclass=Singleton):
    def __init__(self, consumers: List[BaseComsumer]) -> None:
        self.consumers = consumers

    def start_all(self):
        for consumer in self.consumers:
            consumer.start()

    def stop_all(self):
        for consumer in self.consumers:
            consumer.stop()