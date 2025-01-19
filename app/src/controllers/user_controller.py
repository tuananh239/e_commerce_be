# =================================================================================================================
# Feature: user_controller
# =================================================================================================================

"""
    Định nghĩa và triển khai tất cả các API liên quan đến User
"""

# =================================================================================================================

from typing import List,  Union
from fastapi.responses import StreamingResponse
from starlette import status
from fastapi import APIRouter, Depends, Request, Header, UploadFile
from fastapi.param_functions import Body

from app.libs.authentication.bearer_auth import verify_token
from app.libs.exception.exceptions import NotAllowedException
from app.libs.fastapi.decorator import try_catch
from app.libs.fastapi.route import Controller, get_router
from app.libs.fastapi.response import ResponseSuccess
from app.libs.helpers.aes_helper import AESHelper
from app.libs.helpers.validation_helper import ValidationHelper
from app.src.commons.constants.constants import JWT_CONST
from app.src.dependencies.auth_dependency import validate_user_token
from app.src.models.dto.user_dto import UserCreateDTO, UserDTO, UserGetDTO, UserUpdateDTO
from app.src.services.user_service import UserService

# =================================================================================================================

# Declare Element =================================================================================================

# Main ============================================================================================================

user_router = get_router()

user_controller = Controller(
    router=user_router,
    tags=["User"]
)

user_service = UserService()

# Implement API ===================================================================================================
# API Get ---------------------------------------------------------------------------------------------------------
@user_router.get(path="/user/")
@try_catch
async def get_list(
    request: Request,
    params: UserGetDTO = Depends(),
    user = Depends(validate_user_token)
):
    if user != 'admin':
        raise NotAllowedException(message='Người dùng này không có quyền.')

    _result, _pagination, _sort = user_service.get(params=params)

    return ResponseSuccess(
        path=request.url.path,
        result=_result,
        pagination=_pagination,
        sort=_sort
    )


# API Get detail by transaction -----------------------------------------------------------------------------------
@user_router.get(path="/user/{user_id}")
@try_catch
async def get_detail(
    request: Request,
    user_id: str = None,
    user = Depends(validate_user_token)
):
    if user != 'admin':
        raise NotAllowedException(message='Người dùng này không có quyền.')

    _result = user_service.get_detail(user_id=user_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )

# API Create ------------------------------------------------------------------------------------------------------
@user_router.post(path="/user/")
@try_catch
async def create(
    request: Request,
    data: UserCreateDTO = Body(...),
    user = Depends(validate_user_token)
):
    if user != 'admin':
        raise NotAllowedException(message='Người dùng này không có quyền.')

    _result = user_service.create(user=data, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


@user_router.post(path="/user/login")
@try_catch
async def login(
    request: Request,
    data: UserCreateDTO = Body(...)
    # user = Depends(validate_user_token)
):
    _result = user_service.login(data)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


#API Update ------------------------------------------------------------------------------------------------------
@user_router.put(path="/user/{user_id}")
@try_catch
async def update(
    request: Request,
    user_id: str = None,
    data: UserUpdateDTO = Body(...),
    user = Depends(validate_user_token)
):
    if user != 'admin':
        raise NotAllowedException(message='Người dùng này không có quyền.')

    user_service.get_detail(user_id=user_id)

    _result = user_service.update(user_id=user_id, user=data)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


#API Remove ------------------------------------------------------------------------------------------------------
@user_router.delete(path="/user/{user_id}")
@try_catch
async def remove(
    request: Request,
    user_id: str = None,
    user = Depends(validate_user_token)
):
    if user != 'admin':
        raise NotAllowedException(message='Người dùng này không có quyền.')

    user_service.get_detail(user_id=user_id)

    _result = user_service.remove(user_id=user_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )
