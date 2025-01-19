# =================================================================================================================
# Feature: petition_controller
# =================================================================================================================

"""
    Định nghĩa và triển khai tất cả các API liên quan đến Petition
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
from app.src.models.dto.petition_dto import PetitionCreateDTO, PetitionDTO, PetitionGetDTO, PetitionUpdateDTO
from app.src.services.decision_service import DecisionService
from app.src.services.petition_service import PetitionService

# =================================================================================================================

# Declare Element =================================================================================================

# Main ============================================================================================================

petition_router = get_router()

petition_controller = Controller(
    router=petition_router,
    tags=["Petition"]
)

petition_service = PetitionService()
decision_service = DecisionService()

# Implement API ===================================================================================================
# API Get ---------------------------------------------------------------------------------------------------------
@petition_router.get(path="/petition/")
@try_catch
async def get_list(
    request: Request,
    params: PetitionGetDTO = Depends(),
    user = Depends(validate_user_token)
):
    _result, _pagination, _sort = petition_service.get(params=params)

    return ResponseSuccess(
        path=request.url.path,
        result=_result,
        pagination=_pagination,
        sort=_sort
    )


# API Get detail by transaction -----------------------------------------------------------------------------------
@petition_router.get(path="/petition/{petition_id}")
@try_catch
async def get_detail(
    request: Request,
    petition_id: str = None,
    user = Depends(validate_user_token)
):
    _result = petition_service.get_detail(petition_id=petition_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )

# API Create ------------------------------------------------------------------------------------------------------
@petition_router.post(path="/petition/")
@try_catch
async def create(
    request: Request,
    data: PetitionCreateDTO = Body(...),
    images: List[UploadFile] = Depends(ValidationHelper.validate_list_image),
    files: List[UploadFile] = Depends(ValidationHelper.validate_list_pdf),
    user = Depends(validate_user_token)
):
    decision_service.get_detail_by_decision_number(data.decision_number)

    _result = petition_service.create(petition=data, images=images, files=files, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


@petition_router.get(path="/petition/{petition_id}/image/{image_id}/{type_image}")
@try_catch
async def get_image_content(
    request: Request,
    petition_id: str = None,
    image_id: str = None,
    type_image: str = 'original',
    user = Depends(validate_user_token)
):
    folder_path = './data/petition'
    
    if type_image == "original":
        with open(f'{folder_path}/{image_id}.enc', 'rb') as enc_file:
            enc_data = enc_file.read()
    if type_image == "thumbnail":
        with open(f'{folder_path}/{image_id}-thumb.enc', 'rb') as enc_file:
            enc_data = enc_file.read()

    decrypted_data = AESHelper.decrypt_image(enc_data)

    import io
    return StreamingResponse(
        io.BytesIO(decrypted_data),
        media_type='image/png'
    )


@petition_router.get(path="/petition/{petition_id}/file/{file_id}")
@try_catch
async def get_file_content(
    request: Request,
    petition_id: str = None,
    file_id: str = None,
    user = Depends(validate_user_token)
):
    folder_path = './data/petition'

    with open(f'{folder_path}/{file_id}.enc', 'rb') as enc_file:
        enc_data = enc_file.read()

    decrypted_data = AESHelper.decrypt_image(enc_data)

    import io
    return StreamingResponse(
        io.BytesIO(decrypted_data),
        media_type='application/pdf'
    )


#API Update ------------------------------------------------------------------------------------------------------
@petition_router.put(path="/petition/{petition_id}")
@try_catch
async def update(
    request: Request,
    petition_id: str = None,
    data: PetitionUpdateDTO = Body(...),
    images: List[UploadFile] = Depends(ValidationHelper.validate_list_image),
    files: List[UploadFile] = Depends(ValidationHelper.validate_list_pdf),
    user = Depends(validate_user_token)
):
    petition_service.get_detail(petition_id=petition_id)

    _result = petition_service.update(petition_id=petition_id, petition=data, images=images, files=files, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


#API Remove ------------------------------------------------------------------------------------------------------
@petition_router.delete(path="/petition/{petition_id}")
@try_catch
async def remove(
    request: Request,
    petition_id: str = None,
    user = Depends(validate_user_token)
):
    petition_service.get_detail(petition_id=petition_id)

    _result = petition_service.remove(petition_id=petition_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )
