# ===========================================================================================
# Observer
# Dev: anh.vu
# ===========================================================================================

"""
    Class này sử dụng để khởi tạo duy nhất một đối tượng cho một class
"""

# ===========================================================================================

# ===========================================================================================

# Main class ================================================================================
class Observer():
    def __init__(self) -> None:
        self.events = {}

    
    def add_event(self, event: str):
        self.events[event] = []

    
    def subscribe(self, event: str, function):
        self.events[event].append(function)

    
    @staticmethod
    def emit(event):
        def decorator(handler):
            def wrapper(*args, **kwargs):
                handler(*args, **kwargs)
            
            return wrapper
        return decorator

