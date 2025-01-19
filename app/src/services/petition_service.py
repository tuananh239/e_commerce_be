# =================================================================================================================
# Feature: petition_service
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

from app.src.models.dto.petition_dto import PetitionCreateDTO, PetitionDTO, PetitionGetDTO, File
from app.src.models.entity.petition_entity import PetitionEntity
from app.src.repositories.petition_repository import PetitionRepository

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================
class PetitionService(metaclass=Singleton):
    def __init__(self) -> None:
        """"""
        self.__petition_repository = PetitionRepository()

    def create(self, petition: PetitionCreateDTO, images: List[UploadFile], files: List[UploadFile], username: str):
        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)
        list_image_id = []
        list_file_id = []

        folder_data_path = './data'
        if not os.path.exists(folder_data_path):
            # Create the folder
            os.makedirs(folder_data_path)

        folder_petition_path = './data/petition'
        if not os.path.exists(folder_petition_path):
            # Create the folder
            os.makedirs(folder_petition_path)

        for image in images:
            image_bytes = image.file.read()
            image_data = Image.open(BytesIO(image_bytes))
            thumb_bytes = ImageHelper.resize_image(image=image_data)
            id_image = str(uuid.uuid4())
            id_thumb = id_image + "-thumb"
            encrypted_image_path = f'./data/petition/{id_image}.enc'
            encrypted_thumb_path = f'./data/petition/{id_thumb}.enc'
            AESHelper.encrypt_image(image_bytes, encrypted_image_path)
            AESHelper.encrypt_image(thumb_bytes, encrypted_thumb_path)
            list_image_id.append(id_image)

        for file in files:
            file_bytes = file.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/petition/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            list_file_id.append(File(name=file.filename, file_id=id_file))

        _petition_entity = PetitionEntity(
            **petition.__dict__
        )

        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

        _petition_entity.list_image_id = list_image_id
        _petition_entity.list_file_id = list_file_id
        _petition_entity.created_by = username
        _petition_entity.created_time = _timestamp_now
        _petition_entity.modified_by = username
        _petition_entity.modified_time = _timestamp_now
        _petition_entity.is_active = True

        _res = self.__petition_repository.create(petition_data=_petition_entity)

        return _res
    

    def get(self, params: PetitionGetDTO):
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

        _result = self.__petition_repository.get(
            search=_search,
            sort=_sort,
            filter=_filter,
            pagination=_pagination
        )

        if _result:
            _result = [PetitionDTO(**petition.__dict__) for petition in _result]

        _total_records = self.__petition_repository.count_document(
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
    

    def get_detail(self, petition_id: str):
        _petition_entity = self.__petition_repository.get_detail(petition_id=petition_id)

        if _petition_entity == None:
            raise NotFoundException(message='Không tìm thấy đơn xin cấp phép \'{petition_id}\'.')
        
        _petition_dto = PetitionDTO(
            **_petition_entity.__dict__
        )
        
        return _petition_dto
    

    def update(self, petition_id: str, petition: PetitionDTO, images: List[UploadFile], files: List[UploadFile], username: str):
        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

        _petition_entity = PetitionEntity(**petition.__dict__)
        _petition_entity.modified_by = username
        _petition_entity.modified_time = _timestamp_now

        folder_data_path = './data'
        if not os.path.exists(folder_data_path):
            # Create the folder
            os.makedirs(folder_data_path)

        folder_petition_path = './data/petition'
        if not os.path.exists(folder_petition_path):
            # Create the folder
            os.makedirs(folder_petition_path)

        for image in images:
            image_bytes = image.file.read()
            image_data = Image.open(BytesIO(image_bytes))
            thumb_bytes = ImageHelper.resize_image(image=image_data)
            id_image = str(uuid.uuid4())
            id_thumb = id_image + "-thumb"
            encrypted_image_path = f'./data/petition/{id_image}.enc'
            encrypted_thumb_path = f'./data/petition/{id_thumb}.enc'
            AESHelper.encrypt_image(image_bytes, encrypted_image_path)
            AESHelper.encrypt_image(thumb_bytes, encrypted_thumb_path)
            _petition_entity.list_image_id.append(id_image)


        for file in files:
            file_bytes = file.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/petition/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            _petition_entity.list_file_id.append(File(name=file.filename, file_id=id_file))

        self.__petition_repository.update(petition_id=petition_id, petition_data=_petition_entity)

        _petition_entity = self.get_detail(petition_id=petition_id)
        
        _petition_dto = PetitionDTO(
            **_petition_entity.__dict__
        )
        
        return _petition_dto
    

    def remove(self, petition_id: str):

        self.__petition_repository.remove(petition_id=petition_id)
        
        return True