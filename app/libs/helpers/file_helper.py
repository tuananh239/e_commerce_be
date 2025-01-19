# ===========================================================================================
# FileHelper
# Dev: anh.vu
# ===========================================================================================

# ===========================================================================================

import re

from app.libs.pattern.creational.singleton import Singleton

# ===========================================================================================

IMAGE_CONTENT_TYPE = ["IMAGE/JPG", "IMAGE/JPEG", "IMAGE/PNG", "IMAGE/TIFF", "IMAGE/JFIF"]

B_UNIT = 1
KB_UNIT = 2 ** 10
MB_UNIT = 2 ** 20
GB_UNIT = 2 ** 30

# Main class ================================================================================


class FileHelper(metaclass=Singleton):
    """
        Class này triển khai các phương thức hỗ trợ thao tác với file
    """
    def __init__(self) -> None:
        """"""


    @staticmethod
    def is_pdf_data(file_data):
        """
            Kiểm tra dữ liệu có phải là file pdf không
        """
        try:
            # Find the header
            _match_header = re.search(rb"%PDF-\d\.\d", file_data)
            # Find the trailer
            _match_trailer = re.search(rb"%%EOF", file_data)
            return _match_header and _match_trailer
        except Exception:
            return False
        

    @staticmethod
    def get_size_file_data(file_data, unit=None):
        """
            Trả về dung lượng của file\n
            Đầu vào:\n
                - file_data: dữ liệu dạng bytes của file\n
                - unit: đơn vị (KB, MB, GB)\n
            Đầu ra: Dung lượng của file
        """
        if unit in [B_UNIT, KB_UNIT, MB_UNIT, GB_UNIT]:
            return len(file_data)/unit, unit

        _file_size = len(file_data)
        unit = "B"

        if _file_size > GB_UNIT:
            _file_size = round(_file_size/GB_UNIT, 2)
            unit = "GB"
        elif _file_size > MB_UNIT:
            _file_size = round(_file_size/MB_UNIT, 2)
            unit = "MB"
        elif _file_size > KB_UNIT:
            _file_size = round(_file_size/KB_UNIT, 2)
            unit = "KB"
        else:
            """"""
        
        return _file_size, unit
