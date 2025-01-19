# =================================================================================================================
# Feature: constants
# Dev: anhvt9
# Start Date: 16/03/2023
# Maintain Date: 16/03/2023
# =================================================================================================================

"""
    Description
"""

# =================================================================================================================

from app.src.commons.constants.init_const.app_const import AppConstants
from app.src.commons.constants.init_const.mongodb_const import MongoDbConstants
from app.src.commons.constants.init_const.jwt_const import JWTConstants

# Declare Element =================================================================================================

APP_CONST = AppConstants()
JWT_CONST = JWTConstants()
MONGODB_CONST = MongoDbConstants()