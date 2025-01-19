# ===========================================================================================
# Fast API App
# Dev: anh.vu
# ===========================================================================================

"""
    Cấu hình riêng cho fastapi app. Các thành phần:
"""

# ===========================================================================================

import re
from pymongo import MongoClient

# ===========================================================================================

# Main ======================================================================================

class BaseRepository():
    """
        * Class này được sử dụng để định nghĩa các phương thức(method) thao tác với việc\n
        kết nối và xử lý với MongoDB\n
    """

    def _get_connection(self, mongodb_server, database_name):
        MONGODB_SERVER = mongodb_server
        DATABASE_NAME = database_name
        try:
            mongo_client = MongoClient(MONGODB_SERVER)
            db_connection = mongo_client[DATABASE_NAME]
            return db_connection
        except Exception as e:
            """"""
            # logging.error(
            #     f"Can't connect to Mongo server {MONGODB_SERVER} - db name {DATABASE_NAME} "
            #     f" error. - Caused by:  [{ee.__str__()}]")

    def _get_client(self, mongodb_server):
        MONGODB_SERVER = mongodb_server
        try:
            mongo_client = MongoClient(MONGODB_SERVER)
            return mongo_client
        except Exception as e:
            """"""
            # logging.error(
            #     f"Can't connect to Mongo server {MONGODB_SERVER}"
            #     f" error. - Caused by:  [{ee.__str__()}]")

    
    def _approximate_search(self, value):
        """
            Tìm kiếm gần đúng\n
        """

        return {'$regex': f'.*{format(re.escape(value))}.*', '$options': 'i'}