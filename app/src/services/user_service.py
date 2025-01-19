# =================================================================================================================
# Feature: user_service
# =================================================================================================================

"""
    Description
"""

# =================================================================================================================

import jwt
import datetime

from math import ceil
from app.libs.exception.exceptions import AuthorizationException, NotAllowedException, NotFoundException
from app.libs.fastapi.request import Filtering, Pagination, ResponsePagination, Sorting
from app.libs.pattern.creational.singleton import Singleton
from app.libs.helpers.time_helper import TimeHelper, MILISECOND

from app.src.commons.constants.constants import JWT_CONST
from app.src.models.dto.user_dto import UserCreateDTO, UserDTO, UserGetDTO
from app.src.models.entity.user_entity import UserEntity
from app.src.repositories.user_repository import UserRepository

# Declare Element =================================================================================================

# Implement =======================================================================================================

# Sub class =======================================================================================================

# Main class ======================================================================================================
class UserService(metaclass=Singleton):
    def __init__(self) -> None:
        """"""
        self.__user_repository = UserRepository()

    def create(self, user: UserCreateDTO, username):
        _user_detail = self.__user_repository.get_detail_by_user(user=user.email)

        if _user_detail:
            raise NotAllowedException(message=f'{user.email} đã tồn tại.')

        _timestamp_now = TimeHelper.get_timestamp_now(level=MILISECOND)

        _user_entity = UserEntity(
            **user.__dict__
        )

        _user_entity.role = "USER"
        _user_entity.created_time = _timestamp_now
        _user_entity.created_by = username
        _user_entity.modified_time = _timestamp_now
        _user_entity.modified_by = username
        _user_entity.is_active = True

        _res = self.__user_repository.create(user_data=_user_entity)

        return _res
    

    def get(self, params: UserGetDTO):
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

        _result = self.__user_repository.get(
            search=_search,
            sort=_sort,
            filter=_filter,
            pagination=_pagination
        )

        if _result:
            _result = [UserDTO(**user.__dict__) for user in _result]

        _total_records = self.__user_repository.count_document(
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
    

    def get_detail(self, user_id: str):
        _user_entity = self.__user_repository.get_detail(user_id=user_id)

        if _user_entity == None:
            raise NotFoundException(message='Không tìm thấy người dùng \'{user_id}\'.')
        
        _user_dto = UserDTO(
            **_user_entity.__dict__
        )
        
        return _user_dto
    

    def update(self, user_id: str, user: UserDTO):
        self.__user_repository.update(user_id=user_id, user_data=user)

        _user_entity = self.get_detail(user_id=user_id)
        
        _user_dto = UserDTO(
            **_user_entity.__dict__
        )
        
        return _user_dto
    

    def remove(self, user_id: str):

        self.__user_repository.remove(user_id=user_id)
        
        return True
    

    def login(self, user: UserDTO):
        _user_entity = UserEntity(**user.__dict__)

        _user_detail = self.__user_repository.check_valid_user(user=_user_entity)

        if _user_detail == None:
            raise AuthorizationException()

        _payload = {
            'sub': 'user_id',
            'email': getattr(_user_detail, 'email', ''),
            'name': getattr(_user_detail, 'name', ''),
            'phone_number': getattr(_user_detail, 'phone_number', ''),
            'storage': getattr(_user_detail, 'storage', ''),
            'province': getattr(_user_detail, 'province', ''),
            'district': getattr(_user_detail, 'district', ''),
            'address_detail': getattr(_user_detail, 'address_detail', ''),
            'role': _user_detail.role,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }

        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization

        private_key = serialization.load_pem_private_key(
            JWT_CONST.PRIVATE_KEY.encode(),  # Chuyển đổi chuỗi thành byte
            password=None,
            backend=default_backend()
        )

        _token = jwt.encode(payload=_payload, key=private_key, algorithm='RS256')

        return {
            'token': _token
        }