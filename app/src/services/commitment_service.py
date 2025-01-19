# =================================================================================================================
# Feature: commitment_service
# =================================================================================================================

"""
    Description
"""

# =================================================================================================================

import os
import uuid
from PIL import Image
from io import BytesIO

from math import ceil
from typing import List

from fastapi import UploadFile
from app.libs.exception.exceptions import NotFoundException
from app.libs.fastapi.request import Filtering, Pagination, ResponsePagination, Sorting
from app.libs.helpers.aes_helper import AESHelper
from app.libs.helpers.image_helper import ImageHelper
from app.libs.pattern.creational.singleton import Singleton
from app.libs.helpers.time_helper import TimeHelper, MILISECOND

from app.src.models.dto.commitment_dto import CommitmentCreateDTO, CommitmentDTO, CommitmentGetDTO, File
from app.src.models.entity.commitment_entity import CommitmentEntity
from app.src.repositories.commitment_repository import CommitmentRepository

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================
class CommitmentService(metaclass=Singleton):
    def __init__(self) -> None:
        """"""
        self.__commitment_repository = CommitmentRepository()

    def create(self, commitment: CommitmentCreateDTO, images: List[UploadFile], files: List[UploadFile], username: str):
        list_image_id = []
        list_file_id = []

        folder_data_path = './data'
        if not os.path.exists(folder_data_path):
            # Create the folder
            os.makedirs(folder_data_path)

        folder_commitment_path = './data/commitment'
        if not os.path.exists(folder_commitment_path):
            # Create the folder
            os.makedirs(folder_commitment_path)

        for image in images:
            image_bytes = image.file.read()
            image_data = Image.open(BytesIO(image_bytes))
            thumb_bytes = ImageHelper.resize_image(image=image_data)
            id_image = str(uuid.uuid4())
            id_thumb = id_image + "-thumb"
            encrypted_image_path = f'./data/commitment/{id_image}.enc'
            encrypted_thumb_path = f'./data/commitment/{id_thumb}.enc'
            AESHelper.encrypt_image(image_bytes, encrypted_image_path)
            AESHelper.encrypt_image(thumb_bytes, encrypted_thumb_path)
            list_image_id.append(id_image)

        for file in files:
            file_bytes = file.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/commitment/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            list_file_id.append(File(name=file.filename, file_id=id_file))


        _commitment_entity = CommitmentEntity(
            **commitment.__dict__
        )

        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

        _commitment_entity.list_image_id = list_image_id
        _commitment_entity.list_file_id = list_file_id
        _commitment_entity.created_by = username
        _commitment_entity.created_time = _timestamp_now
        _commitment_entity.modified_by = username
        _commitment_entity.modified_time = _timestamp_now
        _commitment_entity.is_active = True

        _res = self.__commitment_repository.create(commitment_data=_commitment_entity)

        return _res
    

    def get(self, params: CommitmentGetDTO):
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

        _result = self.__commitment_repository.get(
            search=_search,
            sort=_sort,
            filter=_filter,
            pagination=_pagination
        )

        if _result:
            _result = [CommitmentDTO(**commitment.__dict__) for commitment in _result]

        _total_records = self.__commitment_repository.count_document(
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
    

    def get_detail(self, commitment_id: str):
        _commitment_entity = self.__commitment_repository.get_detail(commitment_id=commitment_id)

        if _commitment_entity == None:
            raise NotFoundException(message=f"Không tìm thấy cam kết \'{commitment_id}\'.")
        
        _commitment_dto = CommitmentDTO(
            **_commitment_entity.__dict__
        )
        
        return _commitment_dto
    

    def update(self, commitment_id: str, commitment: CommitmentDTO, images: List[UploadFile], files: List[UploadFile], username: str):
        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

        _commitment_entity = CommitmentEntity(**commitment.__dict__)
        _commitment_entity.modified_by = username
        _commitment_entity.modified_time = _timestamp_now

        folder_data_path = './data'
        if not os.path.exists(folder_data_path):
            # Create the folder
            os.makedirs(folder_data_path)

        folder_commitment_path = './data/commitment'
        if not os.path.exists(folder_commitment_path):
            # Create the folder
            os.makedirs(folder_commitment_path)

        for image in images:
            image_bytes = image.file.read()
            image_data = Image.open(BytesIO(image_bytes))
            thumb_bytes = ImageHelper.resize_image(image=image_data)
            id_image = str(uuid.uuid4())
            id_thumb = id_image + "-thumb"
            encrypted_image_path = f'./data/commitment/{id_image}.enc'
            encrypted_thumb_path = f'./data/commitment/{id_thumb}.enc'
            AESHelper.encrypt_image(image_bytes, encrypted_image_path)
            AESHelper.encrypt_image(thumb_bytes, encrypted_thumb_path)
            _commitment_entity.list_image_id.append(id_image)


        for file in files:
            file_bytes = file.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/commitment/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            _commitment_entity.list_file_id.append(File(name=file.filename, file_id=id_file))


        self.__commitment_repository.update(commitment_id=commitment_id, commitment_data=_commitment_entity)

        _commitment_entity = self.get_detail(commitment_id=commitment_id)
        
        _commitment_dto = CommitmentDTO(
            **_commitment_entity.__dict__
        )
        
        return _commitment_dto
    

    def remove(self, commitment_id: str):

        self.__commitment_repository.remove(commitment_id=commitment_id)
        
        return True