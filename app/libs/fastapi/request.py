# ===========================================================================================
# Request Model
# Dev: anh.vu
# ===========================================================================================

import re

from math import ceil
from bson.objectid import ObjectId

from app.libs.exception.exceptions import NotFoundException
from app.libs.exception.soa_error import SOA

# ===========================================================================================

# Main class ================================================================================
class Sorting():
    """
        Mô tả các thông tin liên quan đến sắp xếp kết quả bao gồm:\n
            - Trường sắp xếp\n
            - Thứ tự sắp xếp\n
    """
    def __init__(self, sort_by="_id", sort="desc"):
        self.sort_by = sort_by
        self.sort = 1 if sort == "asc" else -1


class Filtering():
    """
        Mô tả các thông tiên liên quan đến bộ lọc kết quả bao gồm:\n
            - Data: Thông tin lọc theo từng yêu cầu\n
            - Time from: Thời gian bắt đầu tìm kiếm\n
            - Time to: thời gian kết thúc tìm kiếm\n
    """
    def __init__(self, data=None, time_from=None, time_to=None):
        self.data = data if data is not None else {}
        self.time_from = time_from
        self.time_to = time_to
        if "_id" in self.data:
            data['_id'] = ObjectId(data['_id'])
        
    def approximate_search(self):
        """
            Tìm kiếm gần đúng\n
        """
        _filter = {}
        
        if isinstance(self.data, dict):
            for key, value in self.data.items():
                if len(key.split(".")) == 1:
                    if (isinstance(value, str)):
                        _filter[key] = {'$regex': f'.*{format(re.escape(value))}.*', '$options': 'i'}
                    if (isinstance(value, int)):
                        _filter[key] = value

        return _filter


class Pagination():
    """
        Mô tả các thông tin liên quan đến phân trang kết quả bao gồm:\n
            - Số trang\n
            - Số phần tử của 1 trang\n
    """
    def __init__(self, page=1, size=0, is_paging=True):
        self.page = page
        self.size = size if is_paging == True else 0
        self.skip = size*(page - 1) if is_paging == True else 0


class ResponsePagination():
    """
        Mô tả các thông tin phân trang cho kết quả tìm kiếm danh sách
    """
    def __init__(self, page=1, limit=0, total_records=0, total_page=0):
        self.page = page
        self.limit = limit
        self.total_records = total_records
        if total_records != 0 and limit != 0:
            self.total_page = ceil(total_records/limit)
        else:
            self.total_page = total_page

        if self.page != 1 and self.page > self.total_page:
            raise NotFoundException(message=f"Trang {self.page} không tồn tại!")
