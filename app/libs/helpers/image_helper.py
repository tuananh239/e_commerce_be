# ===========================================================================================
# ImageHelper
# Dev: anh.vu
# ===========================================================================================

# ===========================================================================================

import io
import math

from PIL import Image

from app.libs.pattern.creational.singleton import Singleton

# ===========================================================================================

IMAGE_CONTENT_TYPE = ["IMAGE/JPG", "IMAGE/JPEG", "IMAGE/PNG", "IMAGE/TIFF", "IMAGE/JFIF"]

B_UNIT = 1
KB_UNIT = 2 ** 10
MB_UNIT = 2 ** 20
GB_UNIT = 2 ** 30

# Main class ================================================================================


class ImageHelper(metaclass=Singleton):
    """
        Class này triển khai các phương thức hỗ trợ thao tác với hình ảnh
    """
    def __init__(self) -> None:
        """"""


    @staticmethod
    def is_image_data(image_data):
        """
            Kiểm tra dữ liệu có phải là ảnh không
        """
        try:
            with Image.open(io.BytesIO(image_data)):
                return True
        except Exception:
            return False
        

    @staticmethod
    def get_size_image_data(image_data, unit=None):
        """
            Trả về dung lượng của ảnh\n
            Đầu vào:\n
                - image_data: dữ liệu dạng bytes của ảnh\n
                - unit: đơn vị (KB, MB, GB)\n
            Đầu ra: Dung lượng của ảnh
        """
        if unit in [B_UNIT, KB_UNIT, MB_UNIT, GB_UNIT]:
            return len(image_data)/unit, unit

        _image_size = len(image_data)
        unit = B_UNIT

        if _image_size > GB_UNIT:
            _image_size = round(_image_size/GB_UNIT, 2)
            unit = "GB"
        elif _image_size > MB_UNIT:
            _image_size = round(_image_size/MB_UNIT, 2)
            unit = "MB"
        elif _image_size > KB_UNIT:
            _image_size = round(_image_size/KB_UNIT, 2)
            unit = "KB"
        else:
            """"""
        
        return _image_size, unit
    

    @staticmethod
    def set_dpi(image: Image, dpi: tuple):
        """
            Thay đổi DPI của ảnh
        """
        _width, _heigh = image.size
        if image and 'dpi' in image.info and image.info['dpi']:
            _old_width_dpi, _old_height_dpi = image.info['dpi']
            _new_width_dpi, _new_height_dpi = dpi
            if _old_width_dpi >= _new_width_dpi:
                _scale_width = _old_width_dpi / _new_width_dpi
            else:
                _scale_width = 1
            if _old_height_dpi >= _new_height_dpi:
                _scale_height = _old_height_dpi / _new_height_dpi
            else:
                _scale_height = 1
            image = image.resize((math.ceil(_width / _scale_width), math.ceil(_heigh / _scale_height)),
                                 Image.ANTIALIAS)
        return image
    

    @staticmethod
    def resize_image(image: Image, pixel=128):
        # Kích thước mong muốn cho thumbnail
        desired_width = pixel
        desired_height = pixel

        # Tính toán tỷ lệ khung hình
        img_ratio = image.width / image.height
        thumbnail_ratio = desired_width / desired_height

        if img_ratio > thumbnail_ratio:
            # Nếu ảnh gốc rộng hơn thumbnail, điều chỉnh chiều rộng
            new_width = desired_width
            new_height = int(desired_width / img_ratio)
        else:
            # Nếu ảnh gốc cao hơn thumbnail, điều chỉnh chiều cao
            new_height = desired_height
            new_width = int(desired_height * img_ratio)

        # Thay đổi kích thước ảnh
        img_resized = image.resize((new_width, new_height), Image.LANCZOS)

        byte_io = io.BytesIO()
        img_resized.save(byte_io, format='JPEG')  # Hoặc PNG, tùy theo định dạng bạn muốn
        byte_data_resized = byte_io.getvalue()
        byte_io.close()

        return byte_data_resized
        

    @staticmethod
    def get_resolution(image: Image):
        """
            Trả về kích thước của ảnh
        """
        return f'{image.size[0]}x{image.size[1]}'
