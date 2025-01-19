# =================================================================================================================
# Feature: app_const
# Dev: anhvt9
# Start Date: 16/03/2023
# Maintain Date: 16/03/2023
# =================================================================================================================

"""
    Description
"""

# =================================================================================================================

import decouple

from app.libs.pattern.creational.constant import Constant
from app.libs.pattern.creational.singleton import Singleton

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================

class AppConstants(Constant, metaclass=Singleton):
    """
        Quản lý tất các các const của Application
    """
    NAME = str(decouple.config('APP_NAME'))
    TITLE = str(decouple.config('APP_TITLE'))
    DESCRIPTION = str(decouple.config('APP_DESCRIPTION'))
    CONTEXT_ROOT = str(decouple.config('APP_CONTEXT_ROOT'))
    HOST = str(decouple.config('APP_HOST'))
    PORT = int(decouple.config('APP_PORT'))
    VERSION = str(decouple.config('APP_VERSION'))
    LOG_LEVEL = str(decouple.config('APP_LOG_LEVEL'))