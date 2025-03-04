# ===========================================================================================
# Singleton
# Dev: anh.vu
# ===========================================================================================

"""
    Class này sử dụng để khởi tạo duy nhất một đối tượng cho một class
"""

# ===========================================================================================

# ===========================================================================================

# Main class ================================================================================
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
