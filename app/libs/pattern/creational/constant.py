# ===========================================================================================
# Constants Pattern
# Dev: anh.vu
# ===========================================================================================

# Main class ================================================================================
class Constant():
    """
        Tạo ra một đối tượng không thể thay đổi giá trị
    """

    def __setattr__(self, __name: str, __value) -> None:
        """Không thay đổi giá trị"""