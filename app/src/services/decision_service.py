# =================================================================================================================
# Feature: decision_service
# =================================================================================================================

"""
    Description
"""

# =================================================================================================================

import os
import uuid
import zipfile
from datetime import datetime
from fastapi.responses import StreamingResponse
import pandas as pd
from PIL import Image
from io import BytesIO

from math import ceil
from typing import List

from fastapi import UploadFile
from app.libs.exception.exceptions import NotAllowedException, NotFoundException
from app.libs.fastapi.request import Filtering, Pagination, ResponsePagination, Sorting
from app.libs.helpers.aes_helper import AESHelper
from app.libs.helpers.image_helper import ImageHelper
from app.libs.pattern.creational.singleton import Singleton
from app.libs.helpers.time_helper import TimeHelper, MILISECOND

from app.src.models.dto.decision_dto import DecisionCreateDTO, DecisionDTO, DecisionGetDTO, DecisionUpdateDTO, File
from app.src.models.entity.decision_entity import DecisionEntity
from app.src.repositories.decision_repository import DecisionRepository

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================
class DecisionService(metaclass=Singleton):
    def __init__(self) -> None:
        """"""
        self.__decision_repository = DecisionRepository()

    def create(self, decision: DecisionCreateDTO, images: List[UploadFile], files: List[UploadFile], commitments: List[UploadFile], petitions: List[UploadFile], username):
        _decision_detail = self.__decision_repository.get_detail_by_decision_number(decision_number=decision.decision_number)

        if _decision_detail:
            raise NotAllowedException(message=f'Số quyết định \'{_decision_detail.decision_number}\' đã tồn tại.')

        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)
        list_image_id = []
        list_file_id = []
        list_commitment_id = []
        list_petition_id = []

        folder_data_path = './data'
        if not os.path.exists(folder_data_path):
            # Create the folder
            os.makedirs(folder_data_path)

        folder_decision_path = './data/decision'
        if not os.path.exists(folder_decision_path):
            # Create the folder
            os.makedirs(folder_decision_path)

        folder_commitment_path = './data/commitment'
        if not os.path.exists(folder_commitment_path):
            # Create the folder
            os.makedirs(folder_commitment_path)

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
            encrypted_image_path = f'./data/decision/{id_image}.enc'
            encrypted_thumb_path = f'./data/decision/{id_thumb}.enc'
            AESHelper.encrypt_image(image_bytes, encrypted_image_path)
            AESHelper.encrypt_image(thumb_bytes, encrypted_thumb_path)
            list_image_id.append(id_image)

        
        for file in files:
            file_bytes = file.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/decision/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            list_file_id.append(File(name=file.filename, file_id=id_file))

        for commitment in commitments:
            file_bytes = commitment.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/commitment/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            list_commitment_id.append(File(name=commitment.filename, file_id=id_file))

        
        for petition in petitions:
            file_bytes = petition.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/petition/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            list_petition_id.append(File(name=petition.filename, file_id=id_file))


        _decision_entity = DecisionEntity(
            **decision.__dict__
        )


        _decision_entity.list_image_id = list_image_id
        _decision_entity.list_file_id = list_file_id
        _decision_entity.list_commitment_id = list_commitment_id
        _decision_entity.list_petition_id = list_petition_id
        _decision_entity.created_by = username
        _decision_entity.created_time = _timestamp_now
        _decision_entity.modified_by = username
        _decision_entity.modified_time = _timestamp_now
        _decision_entity.is_active = True

        _res = self.__decision_repository.create(decision_data=_decision_entity)

        return _res
    

    def get(self, params: DecisionGetDTO):
        _search = params.search

        _sort = Sorting(
            sort_by=params.sort_by,
            sort=params.sort
        )

        _data = {

        }

        if params.decision_number != None:
            _data['decision_number'] = params.decision_number
        if params.decision_date != None:
            _data['decision_date'] = params.decision_date
        if params.unit != None:
            _data['unit'] = params.unit

        _filter = Filtering(
            time_from=params.time_from,
            time_to=params.time_to,
            data=_data
        )

        _pagination = Pagination(
            page=params.page,
            size=params.size
        )

        _result = self.__decision_repository.get(
            search=_search,
            sort=_sort,
            filter=_filter,
            pagination=_pagination
        )

        if _result:
            _result = [DecisionDTO(**decision.__dict__) for decision in _result]

        _total_records = self.__decision_repository.count_document(
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
    

    def export(self, params: DecisionGetDTO):
        params.page = 1
        params.size = 0

        _result, _pagination, _sort = self.get(params=params)

        data = []


        for decision in _result:
            num_image = 0
            num_file = 0
            num_petition = 0
            num_commitment = 0
            if decision.list_image_id != None:
                num_image = len(decision.list_image_id)

            if decision.list_file_id != None:
                num_file = len(decision.list_file_id)

            if decision.list_petition_id != None:
                num_petition = len(decision.list_petition_id)

            if decision.list_commitment_id != None:
                num_commitment = len(decision.list_commitment_id)
                
            data.append({
                "Số quyết định": decision.decision_number,
                "Ngày quyết định": datetime.fromtimestamp(decision.decision_date/1000).strftime('%Y-%m-%d'),
                "Đơn vị": decision.unit,
                "Địa chỉ": decision.address,
                "Số lượng máy tính": decision.number_computer,
                "Hình thức kết nối": decision.connection_type,
                "Đơn vị cung cấp": decision.internet_carrier,
                "Mục đích sử dụng": decision.intended_use,
                "signer": decision.signer,
                "Người ký": decision.name,
                "Số lượng ảnh": num_image,
                "Số lượng pdf": num_file,
                "Số lượng bản cảm kết":num_commitment,
                "Số lượng đơn xin cấp phép": num_petition,
                "Tình trạng": decision.status,
                "Tạo bởi": decision.created_by,
                "Thời gian tạo": datetime.fromtimestamp(decision.created_time/1000).strftime('%Y-%m-%d')
            })

        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False, engine="openpyxl")
        output.seek(0)  # Đặt con trỏ về đầu file

        # Trả về file Excel dưới dạng streaming response
        return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=decisions.xlsx"})
    

    def get_detail(self, decision_id: str):
        _decision_entity = self.__decision_repository.get_detail(decision_id=decision_id)

        if _decision_entity == None:
            raise NotFoundException(message='Không tìm thấy quyết định \'{decision_id}\'.')
        
        _decision_dto = DecisionDTO(
            **_decision_entity.__dict__
        )
        
        return _decision_dto
    
    
    def export_detail(self, decision_id):
        decision = self.get_detail(decision_id=decision_id)

        data = []
        data.append({
            "Số quyết định": decision.decision_number,
            "Ngày quyết định": datetime.fromtimestamp(decision.decision_date/1000).strftime('%Y-%m-%d'),
            "Đơn vị": decision.unit,
            "Địa chỉ": decision.address,
            "Số lượng máy tính": decision.number_computer,
            "Hình thức kết nối": decision.connection_type,
            "Đơn vị cung cấp": decision.internet_carrier,
            "Mục đích sử dụng": decision.intended_use,
            "signer": decision.signer,
            "Người ký": decision.name,
            "Số lượng ảnh": len(decision.list_image_id),
            "Số lượng pdf": len(decision.list_file_id),
            "Số lượng bản cảm kết":len(decision.list_commitment_id),
            "Số lượng đơn xin cấp phép": len(decision.list_petition_id),
            "Tình trạng": decision.status,
            "Tạo bởi": decision.created_by,
            "Thời gian tạo": datetime.fromtimestamp(decision.created_time/1000).strftime('%Y-%m-%d')
        })


        # Tạo một BytesIO object để lưu trữ file zip
        zip_buffer = BytesIO()

        df = pd.DataFrame(data)
        output = BytesIO()
        df.to_excel(output, index=False, engine="openpyxl")
        output.seek(0)  # Đặt con trỏ về đầu file
        import io
        # Tạo một file zip trong bộ nhớ
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Thêm từng file vào trong file zip
            zip_file.writestr(f"{decision.decision_number}.xlsx", output.read())

            for index, image in enumerate(decision.list_image_id):
                folder_path = './data/decision'
                with open(f'{folder_path}/{image}.enc', 'rb') as enc_file:
                    enc_data = enc_file.read()

                decrypted_data = AESHelper.decrypt_image(enc_data)

                zip_file.writestr(f"anh_{str(index)}.jpg", decrypted_data)

            for index, file in enumerate(decision.list_file_id):
                folder_path = './data/decision'
                with open(f'{folder_path}/{file.file_id}.enc', 'rb') as enc_file:
                    enc_data = enc_file.read()

                decrypted_data = AESHelper.decrypt_image(enc_data)

                zip_file.writestr(file.name, decrypted_data)

            for index, commitment in enumerate(decision.list_commitment_id):
                folder_path = './data/commitment'
                with open(f'{folder_path}/{commitment.file_id}.enc', 'rb') as enc_file:
                    enc_data = enc_file.read()

                decrypted_data = AESHelper.decrypt_image(enc_data)

                zip_file.writestr(commitment.name, decrypted_data)

            for index, petition in enumerate(decision.list_petition_id):
                folder_path = './data/petition'
                with open(f'{folder_path}/{petition.file_id}.enc', 'rb') as enc_file:
                    enc_data = enc_file.read()

                decrypted_data = AESHelper.decrypt_image(enc_data)

                zip_file.writestr(petition.name, decrypted_data)

        # Đặt con trỏ về đầu file zip
        zip_buffer.seek(0)

        # Trả về file zip dưới dạng StreamingResponse
        return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": f"attachment; filename={decision.decision_number}.zip"})


    def get_detail_by_decision_number(self, decision_number: str):
        _decision_entity = self.__decision_repository.get_detail_by_decision_number(decision_number=decision_number)

        if _decision_entity == None:
            raise NotFoundException(message=f"Không tìm thấy quyết định \'{decision_number}\'.")
        
        _decision_dto = DecisionDTO(
            **_decision_entity.__dict__
        )
        
        return _decision_dto
    

    def update(self, decision_id: str, decision: DecisionUpdateDTO, images: List[UploadFile], files: List[UploadFile], commitments: List[UploadFile], petitions: List[UploadFile], username):
        _decision_detail = self.__decision_repository.get_detail(decision_id=decision_id)

        if _decision_detail.decision_number != decision.decision_number:
            _decision_detail = self.__decision_repository.get_detail_by_decision_number(decision_number=decision.decision_number)

            if _decision_detail:
                raise NotAllowedException(message=f'Số quyết định \'{_decision_detail.decision_number}\' đã tồn tại.')

        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

        _decision_entity = DecisionEntity(**decision.__dict__)
        _decision_entity.modified_by = username
        _decision_entity.modified_time = _timestamp_now

        folder_data_path = './data'
        if not os.path.exists(folder_data_path):
            # Create the folder
            os.makedirs(folder_data_path)

        folder_decision_path = './data/decision'
        if not os.path.exists(folder_decision_path):
            # Create the folder
            os.makedirs(folder_decision_path)

        for image in images:
            image_bytes = image.file.read()
            image_data = Image.open(BytesIO(image_bytes))
            thumb_bytes = ImageHelper.resize_image(image=image_data)
            id_image = str(uuid.uuid4())
            id_thumb = id_image + "-thumb"
            encrypted_image_path = f'./data/decision/{id_image}.enc'
            encrypted_thumb_path = f'./data/decision/{id_thumb}.enc'
            AESHelper.encrypt_image(image_bytes, encrypted_image_path)
            AESHelper.encrypt_image(thumb_bytes, encrypted_thumb_path)
            _decision_entity.list_image_id.append(id_image)


        for file in files:
            file_bytes = file.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/decision/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            _decision_entity.list_file_id.append(File(name=file.filename, file_id=id_file))

        for commitment in commitments:
            file_bytes = commitment.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/commitment/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            _decision_entity.list_commitment_id.append(File(name=commitment.filename, file_id=id_file))

        
        for petition in petitions:
            file_bytes = petition.file.read()
            id_file = str(uuid.uuid4())
            encrypted_file_path = f'./data/petition/{id_file}.enc'
            AESHelper.encrypt_image(file_bytes, encrypted_file_path)
            _decision_entity.list_petition_id.append(File(name=petition.filename, file_id=id_file))

        self.__decision_repository.update(decision_id=decision_id, decision_data=_decision_entity)

        _decision_entity = self.get_detail(decision_id=decision_id)
        
        _decision_dto = DecisionDTO(
            **_decision_entity.__dict__
        )
        
        return _decision_dto
    

    def remove(self, decision_id: str):

        self.__decision_repository.remove(decision_id=decision_id)
        
        return True