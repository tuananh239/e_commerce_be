# =================================================================================================================
# Feature: mongodb_const
# Dev: anhvt9
# Start Date: 15/11/2023
# Maintain Date: 15/11/2023
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
class MongoDbConnectionConstants(Constant, metaclass=Singleton):
    """
        Định nghĩa tất cả thông tin kết nối của MongoDb
    """
    SERVER = decouple.config('DATABASE_SERVER')


class MongoDbSyntaxConstants(Constant, metaclass=Singleton):
    """
        Định nghĩa tất cả syntax sử dụng trong MongoDb
    """
    OR = "$or"
    SET = "$set"


# Main class ======================================================================================================
class MongoDbConstants(Constant, metaclass=Singleton):
    """
        Quản lý tất cả các const của MongoDB
    """
    CONNECTION = MongoDbConnectionConstants()
    SYNTAX = MongoDbSyntaxConstants()