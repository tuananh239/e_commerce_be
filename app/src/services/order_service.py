# =================================================================================================================
# Feature: order_service
# =================================================================================================================

"""
    Description
"""

# =================================================================================================================

import os
from typing import List
import uuid
from PIL import Image
from io import BytesIO

from math import ceil

from fastapi import UploadFile
from app.libs.exception.exceptions import NotFoundException
from app.libs.fastapi.request import Filtering, Pagination, ResponsePagination, Sorting
from app.libs.helpers.aes_helper import AESHelper
from app.libs.helpers.image_helper import ImageHelper
from app.libs.pattern.creational.singleton import Singleton
from app.libs.helpers.time_helper import TimeHelper, MILISECOND

from app.src.models.dto.order_dto import OrderCreateDTO, OrderDTO, OrderGetDTO
from app.src.models.entity.order_entity import OrderEntity
from app.src.repositories.order_repository import OrderRepository

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================
class OrderService(metaclass=Singleton):
    def __init__(self) -> None:
        """"""
        self.__order_repository = OrderRepository()

    def create(self, order: OrderCreateDTO, image: UploadFile, username: str):
        folder_data_path = './data'
        if not os.path.exists(folder_data_path):
            # Create the folder
            os.makedirs(folder_data_path)

        folder_order_path = './data/order'
        if not os.path.exists(folder_order_path):
            # Create the folder
            os.makedirs(folder_order_path)

        image_bytes = image.file.read()
        image_data = Image.open(BytesIO(image_bytes))
        thumb_bytes = ImageHelper.resize_image(image=image_data)
        id_image = str(uuid.uuid4())
        id_thumb = id_image + "-thumb"
        encrypted_image_path = f'./data/order/{id_image}.enc'
        encrypted_thumb_path = f'./data/order/{id_thumb}.enc'
        AESHelper.encrypt_image(image_bytes, encrypted_image_path)
        AESHelper.encrypt_image(thumb_bytes, encrypted_thumb_path)

        _order_entity = OrderEntity(
            **order.__dict__
        )

        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)
        _order_code = f"{_timestamp_now}"

        _order_entity.image_order = id_image
        _order_entity.code = _order_code
        _order_entity.created_by = username
        _order_entity.created_time = _timestamp_now
        _order_entity.modified_by = username
        _order_entity.modified_time = _timestamp_now
        _order_entity.is_active = True

        _res = self.__order_repository.create(order_data=_order_entity)

        return _res
    

    def get(self, params: OrderGetDTO):
        _search = params.search

        _sort = Sorting(
            sort_by=params.sort_by,
            sort=params.sort
        )

        _filter = Filtering(
            time_from=params.time_from,
            time_to=params.time_to
        )

        _pagination = Pagination(
            page=params.page,
            size=params.size
        )

        _result = self.__order_repository.get(
            search=_search,
            sort=_sort,
            filter=_filter,
            pagination=_pagination
        )

        if _result:
            _result = [OrderDTO(**order.__dict__) for order in _result]

        _total_records = self.__order_repository.count_document(
            filter=_filter,
            search=_search
        )

        _pagination = ResponsePagination(
            page=_pagination.page,
            limit=_total_records if _pagination.size == 0 else _pagination.size,
            total_records=_total_records,
            total_page=ceil(_total_records / _pagination.size) if _pagination.size > 0 else 1
        )

        return _result, _pagination, _sort
    

    def get_detail(self, order_id: str):
        _order_entity = self.__order_repository.get_detail(order_id=order_id)

        if _order_entity == None:
            raise NotFoundException(message='Không tìm thấy đơn xin cấp phép \'{order_id}\'.')
        
        _order_dto = OrderDTO(
            **_order_entity.__dict__
        )
        
        return _order_dto
    

    def update(self, order_id: str, order: OrderDTO, images: List[UploadFile], files: List[UploadFile], username: str):
        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

        _order_entity = OrderEntity(**order.__dict__)
        _order_entity.modified_by = username
        _order_entity.modified_time = _timestamp_now

        folder_data_path = './data'
        if not os.path.exists(folder_data_path):
            # Create the folder
            os.makedirs(folder_data_path)

        folder_order_path = './data/order'
        if not os.path.exists(folder_order_path):
            # Create the folder
            os.makedirs(folder_order_path)

        for image in images:
            image_bytes = image.file.read()
            image_data = Image.open(BytesIO(image_bytes))
            thumb_bytes = ImageHelper.resize_image(image=image_data)
            id_image = str(uuid.uuid4())
            id_thumb = id_image + "-thumb"
            encrypted_image_path = f'./data/order/{id_image}.enc'
            encrypted_thumb_path = f'./data/order/{id_thumb}.enc'
            AESHelper.encrypt_image(image_bytes, encrypted_image_path)
            AESHelper.encrypt_image(thumb_bytes, encrypted_thumb_path)
            _order_entity.list_image_id.append(id_image)


        for file in files:
            file_bytes = file.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/order/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            _order_entity.list_file_id.append(File(name=file.filename, file_id=id_file))

        self.__order_repository.update(order_id=order_id, order_data=_order_entity)

        _order_entity = self.get_detail(order_id=order_id)
        
        _order_dto = OrderDTO(
            **_order_entity.__dict__
        )
        
        return _order_dto
    

    def remove(self, order_id: str):

        self.__order_repository.remove(order_id=order_id)
        
        return True