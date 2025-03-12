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
from app.src.repositories.config_repository import ConfigRepository
from app.src.repositories.order_repository import OrderRepository
from app.src.repositories.user_repository import UserRepository

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================
class OrderService(metaclass=Singleton):
    def __init__(self) -> None:
        """"""
        self.__order_repository = OrderRepository()
        self.__config_repository = ConfigRepository()
        self.__user_repository = UserRepository()

    def create(self, order: OrderCreateDTO, image: UploadFile, username: str):
        folder_data_path = './data'
        if not os.path.exists(folder_data_path):
            # Create the folder
            os.makedirs(folder_data_path)

        folder_order_path = './data/order'
        if not os.path.exists(folder_order_path):
            # Create the folder
            os.makedirs(folder_order_path)

        id_image = None
        if image:
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

        _order_entity.status="1"
        _order_entity.image_order = id_image
        _order_entity.code = _order_code
        _order_entity.created_by = username
        _order_entity.created_time = _timestamp_now
        _order_entity.modified_by = username
        _order_entity.modified_time = _timestamp_now
        _order_entity.is_active = True

        _res = self.__order_repository.create(order_data=_order_entity)

        return _res
    

    def get(self, params: OrderGetDTO, user):

        _search = params.search

        _sort = Sorting(
            sort_by=params.sort_by,
            sort=params.sort
        )

        _user_detail = self.__user_repository.get_detail_by_user(user=user)

        if _user_detail.role == "ADMIN":
            _filter = Filtering(
                time_from=params.time_from,
                time_to=params.time_to,
                data={
                    "status": params.status
                }
            )
        else:
            _filter = Filtering(
                time_from=params.time_from,
                time_to=params.time_to,
                data={
                    "status": params.status,
                    "created_by": user
                }
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

        _result_dto = []
        if _result:
            _config_entity = self.__config_repository.get_latest()

            for _order_entity in _result:
                _user_entity = self.__user_repository.get_detail_by_user(user=_order_entity.created_by)
                _order_entity.exchange_rate = _config_entity.exchange_rate

                _total_cn_price = 0
                for _product in _order_entity.products:
                    _total_cn_price = _total_cn_price + _product.price * _product.number

                _total_vn_price = _total_cn_price*_config_entity.exchange_rate
                
                _order_fee_percent = 0
                for _option in _config_entity.purchase_fee:

                        if _option.min == 0 and _total_vn_price == 0:
                            _order_fee_percent = _option.value
                            break
                        else:
                            if _total_vn_price > _option.min and _total_vn_price <= _option.max:
                                _order_fee_percent = _option.value
                                break

                _weight_total_fee = 0
                _weight_base_volumn_total_fee = 0
                _weight_rate = 0
                _weight_base_volumn_rate = 0
                if not _order_entity.packages:
                    _order_entity.packages = []
                for _package in _order_entity.packages:
                    for _option in _config_entity.weight:
                        if _package.weight:
                            if _package.weight > _option.min and _package.weight <= _option.max:
                                _weight_rate = _option.value
                                break

                    _package.weight_rate = _weight_rate
                    _package.total_weight_price = _weight_rate*(_package.weight if _package.weight else 0)

                    _weight_total_fee = _weight_total_fee + _package.total_weight_price

                    #
                    for _option in _config_entity.weight:
                        if _package.weight_base_volumn:
                            if _package.weight_base_volumn > _option.min and _package.weight_base_volumn <= _option.max:
                                _weight_base_volumn_rate = _option.value
                                break

                    _package.weight_base_volumn_rate = _weight_base_volumn_rate
                    _package.total_weight_volumn_price = _weight_base_volumn_rate*(_package.weight_base_volumn if _package.weight_base_volumn else 0)

                    _weight_base_volumn_total_fee = _weight_base_volumn_total_fee + _package.total_weight_volumn_price

                _order_entity.weight_fee = _weight_total_fee
                _order_entity.weight_base_volumn = _weight_base_volumn_total_fee

                if _weight_total_fee >= _weight_base_volumn_total_fee:
                    _order_entity.total_weight_fee = _weight_total_fee
                    _order_entity.weight_rate = _weight_rate
                else:
                    _order_entity.total_weight_fee = _weight_base_volumn_total_fee
                    _order_entity.weight_rate = _weight_base_volumn_rate

                _order_entity.item_total_cost = _total_vn_price

                _order_entity.total_fee = _total_vn_price \
                    + _total_vn_price * _order_fee_percent \
                    + (_order_entity.extra_fee if _order_entity.extra_fee != None else 0) \
                    + (_order_entity.ship_cn_fee if _order_entity.ship_cn_fee != None else 0) \
                    + (_order_entity.tally_fee if _order_entity.tally_fee != None else 0) \
                    + (_order_entity.extra_ship_fee if _order_entity.extra_ship_fee != None else 0) \
                    + (_order_entity.wood_package_fee if _order_entity.wood_package_fee != None else 0) \
                    + (_order_entity.total_weight_fee if _order_entity.total_weight_fee != None else 0)
                _order_entity.exchange_rate = _config_entity.exchange_rate
                _order_entity.order_fee_percent = _order_fee_percent
                _order_entity.order_fee = _total_vn_price * _order_fee_percent

                _order_dto = OrderDTO(**_order_entity.__dict__)
                if _user_entity:
                    _order_dto.email = _user_entity.email
                    _order_dto.phone_number = _user_entity.phone_number
                    _order_dto.name = _user_entity.name
                    _order_dto.storage = _user_entity.storage
                    _order_dto.province = _user_entity.province
                    _order_dto.district = _user_entity.district
                    _order_dto.address_detail = _user_entity.address_detail
                    _order_dto.user_storage = _user_entity.storage
                
                _result_dto.append(_order_dto)

            # for order in _result:
                

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

        return _result_dto, _pagination, _sort
    

    def get_detail(self, order_id: str, user=""):
        _order_entity = self.__order_repository.get_detail(order_id=order_id)
        _user_entity = self.__user_repository.get_detail_by_user(user=_order_entity.created_by)
        _config_entity = self.__config_repository.get_latest()

        _order_entity.exchange_rate = _config_entity.exchange_rate

        _total_cn_price = 0
        for _product in _order_entity.products:
            _total_cn_price = _total_cn_price + _product.price * _product.number

        _total_vn_price = _total_cn_price*_config_entity.exchange_rate
        
        _order_fee_percent = 0
        for _option in _config_entity.purchase_fee:

                if _option.min == 0 and _total_vn_price == 0:
                    _order_fee_percent = _option.value
                    break
                else:
                    if _total_vn_price > _option.min and _total_vn_price <= _option.max:
                        _order_fee_percent = _option.value
                        break

        _weight_total_fee = 0
        _weight_base_volumn_total_fee = 0
        _weight_rate = 0
        _weight_base_volumn_rate = 0
        if not _order_entity.packages:
            _order_entity.packages = []
        for _package in _order_entity.packages:
            for _option in _config_entity.weight:
                if _package.weight:
                    if _package.weight > _option.min and _package.weight <= _option.max:
                        _weight_rate = _option.value
                        break

            _package.weight_rate = _weight_rate
            _package.total_weight_price = _weight_rate*(_package.weight if _package.weight else 0)

            _weight_total_fee = _weight_total_fee + _package.total_weight_price

            #
            for _option in _config_entity.weight:
                if _package.weight_base_volumn:
                    if _package.weight_base_volumn > _option.min and _package.weight_base_volumn <= _option.max:
                        _weight_base_volumn_rate = _option.value
                        break

            _package.weight_base_volumn_rate = _weight_base_volumn_rate
            _package.total_weight_volumn_price = _weight_base_volumn_rate*(_package.weight_base_volumn if _package.weight_base_volumn else 0)

            _weight_base_volumn_total_fee = _weight_base_volumn_total_fee + _package.total_weight_volumn_price

        _order_entity.weight_fee = _weight_total_fee
        _order_entity.weight_base_volumn = _weight_base_volumn_total_fee

        if _weight_total_fee >= _weight_base_volumn_total_fee:
            _order_entity.total_weight_fee = _weight_total_fee
            _order_entity.weight_rate = _weight_rate
        else:
            _order_entity.total_weight_fee = _weight_base_volumn_total_fee
            _order_entity.weight_rate = _weight_base_volumn_rate

        _order_entity.item_total_cost = _total_vn_price

        _order_entity.total_fee = _total_vn_price \
            + _total_vn_price * _order_fee_percent \
            + (_order_entity.extra_fee if _order_entity.extra_fee != None else 0) \
            + (_order_entity.ship_cn_fee if _order_entity.ship_cn_fee != None else 0) \
            + (_order_entity.tally_fee if _order_entity.tally_fee != None else 0) \
            + (_order_entity.extra_ship_fee if _order_entity.extra_ship_fee != None else 0) \
            + (_order_entity.wood_package_fee if _order_entity.wood_package_fee != None else 0) \
            + (_order_entity.total_weight_fee if _order_entity.total_weight_fee != None else 0)
        _order_entity.exchange_rate = _config_entity.exchange_rate
        _order_entity.order_fee_percent = _order_fee_percent
        _order_entity.order_fee = _total_vn_price * _order_fee_percent


        if _order_entity == None:
            raise NotFoundException(message='Không tìm thấy đơn xin cấp phép \'{order_id}\'.')
        
        _order_dto = OrderDTO(
            **_order_entity.__dict__
        )

        if _user_entity:
            _order_dto.email = _user_entity.email
            _order_dto.phone_number = _user_entity.phone_number
            _order_dto.name = _user_entity.name
            _order_dto.storage = _user_entity.storage
            _order_dto.province = _user_entity.province
            _order_dto.district = _user_entity.district
            _order_dto.address_detail = _user_entity.address_detail
            _order_dto.user_storage = _user_entity.storage

        
        return _order_dto
    

    def update(self, order_id: str, order: OrderDTO, images: List[UploadFile], username: str):
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

        self.__order_repository.update(order_id=order_id, order_data=_order_entity)

        _order_entity = self.get_detail(order_id=order_id, user=username)
        
        _order_dto = OrderDTO(
            **_order_entity.__dict__
        )
        
        return _order_dto
    

    def remove(self, order_id: str):

        self.__order_repository.remove(order_id=order_id)
        
        return True