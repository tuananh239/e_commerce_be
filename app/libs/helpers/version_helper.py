# ===========================================================================================
# VersionHelper
# Dev: anh.vu
# ===========================================================================================

# ===========================================================================================

# ===========================================================================================

# Main class ================================================================================
class VersionHelper():
    """
        Class này triển khai các phương thức hỗ trợ cho việc quản lý version\n
        Mô tả: x.y.z\n
        x - Major version: tăng khi bạn thực hiện các thay đổi dẫn đến không tương thích ngược\n
        y - Minor version: tăng khi bạn thêm tính năng và vẫn đảm bảo tương thích ngược\n
        z - Patches: tăng khi bạn thực hiện sửa đổi bên trong và vẫn đảm bảo tương thích ngược\n
    """

    @staticmethod
    def new_version():
        """
            Trả về version đầu tiên
        """
        return "1.0.0"
    

    @staticmethod
    def up_major_version(current_version):
        """
            current_version: format x.y.z
        """
        _current_major_version = int(current_version.split(".")[0])
        _new_version = f'{str(_current_major_version + 1)}.0.0'

        return _new_version
    

    @staticmethod
    def up_minor_version(current_version):
        """
            current_version: format x.y.z
        """
        _current_minor_version = int(current_version.split(".")[1])
        _new_version = f'{current_version[0]}.{str(_current_minor_version + 1)}.0'

        return _new_version
    

    @staticmethod
    def up_patches(current_version):
        """
            current_version: format x.y.z
        """
        _current_patches = int(current_version.split(".")[2])
        _new_version = f'{current_version[0]}.{current_version[2]}.{str(_current_patches + 1)}'

        return _new_version
    
