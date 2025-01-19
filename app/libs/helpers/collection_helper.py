from app.libs.pattern.creational.singleton import Singleton


class CollectionHelper(metaclass=Singleton):
    """
            Class này triển khai các phương thức hỗ trợ thao tác với List, Array
        """

    def __init__(self) -> None:
        """"""

    @staticmethod
    def list_none_or_empty(list_object):
        """
            Kiểm tra dữ liệu có phải dạng List & List có chưa p tử hay không
        :param list_object:
        :return: Trả về True nếu List có giá trị None or rỗng
        """
        return True if (list_object is None or len(list_object) == 0) else False
