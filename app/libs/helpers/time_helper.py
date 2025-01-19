# ===========================================================================================
# TimeHelper
# Dev: anh.vu
# ===========================================================================================

# ===========================================================================================

from datetime import datetime, timedelta

# ===========================================================================================

SECOND = "SECOND"
MILISECOND = "MILISECOND"

# ===========================================================================================

# Main class ================================================================================
class TimeHelper():
    """
        Class này triển khai các phương thức hỗ trợ cho việc thao tác xử lý thời gian
    """

    @staticmethod
    def get_timestamp_now(level=SECOND):
        """
            Trả về thời gian hiện tại dạng timestamp
        """
        if level == SECOND:
            timestamp = datetime.timestamp(datetime.today())
        if level == MILISECOND:
            timestamp = datetime.timestamp(datetime.today())*1000
        return int(timestamp)
    

    @staticmethod
    def get_time_now():
        return datetime.now()