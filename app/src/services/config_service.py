# =================================================================================================================
# Feature: config_service
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

from app.src.models.dto.config_dto import ConfigCreateDTO, ConfigDTO, ConfigGetDTO
from app.src.models.entity.config_entity import ConfigEntity
from app.src.repositories.config_repository import ConfigRepository

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================
class ConfigService(metaclass=Singleton):
    def __init__(self) -> None:
        """"""
        self.__config_repository = ConfigRepository()

    def create(self, config: ConfigCreateDTO, username: str):
        _config_entity = ConfigEntity(
            **config.__dict__
        )

        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

        _config_entity.created_by = username
        _config_entity.created_time = _timestamp_now
        _config_entity.modified_by = username
        _config_entity.modified_time = _timestamp_now
        _config_entity.is_active = True

        _res = self.__config_repository.create(config_data=_config_entity)

        return _res
    

    def get(self, params: ConfigGetDTO):
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

        _result = self.__config_repository.get(
            search=_search,
            sort=_sort,
            filter=_filter,
            pagination=_pagination
        )

        if _result:
            _result = [ConfigDTO(**config.__dict__) for config in _result]

        _total_records = self.__config_repository.count_document(
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
    

    def get_detail(self, config_id: str):
        _config_entity = self.__config_repository.get_detail(config_id=config_id)

        if _config_entity == None:
            raise NotFoundException(message='Không tìm thấy đơn xin cấp phép \'{config_id}\'.')
        
        _config_dto = ConfigDTO(
            **_config_entity.__dict__
        )
        
        return _config_dto
    

    def update(self, config_id: str, config: ConfigDTO, username: str):
        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

        _config_entity = ConfigEntity(**config.__dict__)
        _config_entity.modified_by = username
        _config_entity.modified_time = _timestamp_now

        self.__config_repository.update(config_id=config_id, config_data=_config_entity)

        _config_entity = self.get_detail(config_id=config_id)
        
        _config_dto = ConfigDTO(
            **_config_entity.__dict__
        )
        
        return _config_dto
    

    def remove(self, config_id: str):

        self.__config_repository.remove(config_id=config_id)
        
        return True