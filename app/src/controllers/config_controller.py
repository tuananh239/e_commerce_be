# =================================================================================================================
# Feature: oder_controller
# =================================================================================================================

"""
    Định nghĩa và triển khai tất cả các API liên quan đến Config
"""

# =================================================================================================================
from typing import List,  Union
from fastapi.responses import StreamingResponse
from starlette import status
from fastapi import APIRouter, Depends, Request, Header, UploadFile
from fastapi.param_functions import Body

from app.libs.fastapi.decorator import try_catch
from app.libs.fastapi.route import Controller, get_router
from app.libs.fastapi.response import ResponseSuccess
from app.libs.helpers.aes_helper import AESHelper
from app.libs.helpers.validation_helper import ValidationHelper
from app.src.dependencies.auth_dependency import validate_user_token
from app.src.models.dto.config_dto import ConfigDTO, ConfigCreateDTO, ConfigUpdateDTO, ConfigGetDTO
from app.src.services.config_service import ConfigService

# =================================================================================================================

# Declare Element =================================================================================================

# Main ============================================================================================================

config_router = get_router()

config_controller = Controller(
    router=config_router,
    tags=["Config"]
)

config_service = ConfigService()

# Implement API ===================================================================================================
# API Get ---------------------------------------------------------------------------------------------------------
@config_router.get(path="/config/")
@try_catch
async def get_list(
    request: Request,
    params: ConfigGetDTO = Depends(),
    # user = Depends(validate_user_token)
):
    _result, _pagination, _sort = config_service.get(params=params)

    return ResponseSuccess(
        path=request.url.path,
        result=_result,
        pagination=_pagination,
        sort=_sort
    )


@config_router.get(path="/config/latest")
@try_catch
async def get_latest(
    request: Request,
    # user = Depends(validate_user_token)
):
    _params = ConfigGetDTO()
    _params.sort = "desc"
    _result, _pagination, _sort = config_service.get(params=_params)

    _res = None
    if len(_result) > 0:
        _res = _result[0]


    return ResponseSuccess(
        path=request.url.path,
        result=_res
    )


# API Get detail by transaction -----------------------------------------------------------------------------------
@config_router.get(path="/config/{config_id}")
@try_catch
async def get_detail(
    request: Request,
    config_id: str = None,
    # user = Depends(validate_user_token)
):
    _result = config_service.get_detail(config_id=config_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )

# API Create ------------------------------------------------------------------------------------------------------
@config_router.post(path="/config/")
@try_catch
async def create(
    request: Request,
    data: ConfigCreateDTO = Body(...),
    # user = Depends(validate_user_token)
    user = "user"
):

    _result = config_service.create(config=data, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


#API Update ------------------------------------------------------------------------------------------------------
@config_router.put(path="/config/{config_id}")
@try_catch
async def update(
    request: Request,
    config_id: str = None,
    data: ConfigUpdateDTO = Body(...),
    # user = Depends(validate_user_token)
    user= "user"
):
    config_service.get_detail(config_id=config_id)

    _result = config_service.update(config_id=config_id, config=data, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


#API Remove ------------------------------------------------------------------------------------------------------
@config_router.delete(path="/config/{config_id}")
@try_catch
async def remove(
    request: Request,
    config_id: str = None,
    # user = Depends(validate_user_token)
    user="user"
):
    config_service.get_detail(config_id=config_id)

    _result = config_service.remove(config_id=config_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )
