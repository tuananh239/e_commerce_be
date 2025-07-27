# =================================================================================================================
# Feature: cart_service
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

from app.src.models.dto.cart_dto import CartDTO, CartUpdateDTO
from app.src.models.dto.order_dto import ProductDTO
from app.src.models.entity.cart_entity import CartEntity
from app.src.repositories.config_repository import ConfigRepository
from app.src.repositories.cart_repository import CartRepository
from app.src.repositories.user_repository import UserRepository

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================
class CartService(metaclass=Singleton):
    def __init__(self) -> None:
        """"""
        self.__cart_repository = CartRepository()
        self.__config_repository = ConfigRepository()
        self.__user_repository = UserRepository()

    def add_product(self, product: ProductDTO, username: str):
        _cart_entity = self.__cart_repository.get(user=username)

        if _cart_entity == None:
            _cart_entity = CartEntity(
                products=[product]
            )

            _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

            _cart_entity.created_by = username
            _cart_entity.created_time = _timestamp_now
            _cart_entity.modified_by = username
            _cart_entity.modified_time = _timestamp_now
            _cart_entity.is_active = True

            _res = self.__cart_repository.create(cart_data=_cart_entity)

            return _res
        
        else:
            _cart_entity.products.append(product)

            _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

            _cart_entity.modified_by = username
            _cart_entity.modified_time = _timestamp_now

            _res = self.__cart_repository.update(cart_id=_cart_entity.id, cart_data=_cart_entity)

            return _res
    

    def get(self, username):
        _cart_entity = self.__cart_repository.get(user=username)

        _cart_dto = None
        if _cart_entity != None:
            _cart_dto = CartDTO(
                **_cart_entity.__dict__
            )

        return _cart_dto
    

    def update(self, cart_id, card: CartDTO, username: str):
        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

        _cart_entity = CartEntity(**card.__dict__)
        _cart_entity.modified_by = username
        _cart_entity.modified_time = _timestamp_now

        self.__cart_repository.update(cart_id=cart_id, cart_data=_cart_entity)

        _cart_entity = self.get(username=username)
        
        _cart_dto = CartDTO(
            **_cart_entity.__dict__
        )

        return _cart_dto
    

    def remove(self, cart_id: str):

        self.__cart_repository.remove(cart_id=cart_id)
        
        return True