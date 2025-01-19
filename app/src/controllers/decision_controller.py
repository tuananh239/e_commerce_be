# =================================================================================================================
# Feature: decision_controller
# =================================================================================================================

"""
    Định nghĩa và triển khai tất cả các API liên quan đến Decision
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
from app.src.models.dto.decision_dto import DecisionCreateDTO, DecisionDTO, DecisionGetDTO, DecisionUpdateDTO
from app.src.services.decision_service import DecisionService

# =================================================================================================================

# Declare Element =================================================================================================

# Main ============================================================================================================

decision_router = get_router()

decision_controller = Controller(
    router=decision_router,
    tags=["Decision"]
)

decision_service = DecisionService()

# Implement API ===================================================================================================
# API Get ---------------------------------------------------------------------------------------------------------
@decision_router.get(path="/decision/")
@try_catch
async def get_list(
    request: Request,
    params: DecisionGetDTO = Depends(),
    user = Depends(validate_user_token)
):
    _result, _pagination, _sort = decision_service.get(params=params)

    return ResponseSuccess(
        path=request.url.path,
        result=_result,
        pagination=_pagination,
        sort=_sort
    )


@decision_router.get(path="/decision/export")
@try_catch
async def export(
    request: Request,
    params: DecisionGetDTO = Depends(),
    user = Depends(validate_user_token)
):
    _result = decision_service.export(params=params)

    return _result


@decision_router.get(path="/decision/{decision_id}/export")
@try_catch
async def export_detail(
    request: Request,
    decision_id: str = None,
    user = Depends(validate_user_token)
):
    _result = decision_service.export_detail(decision_id=decision_id)

    return _result


# API Get detail by transaction -----------------------------------------------------------------------------------
@decision_router.get(path="/decision/{decision_id}")
@try_catch
async def get_detail(
    request: Request,
    decision_id: str = None,
    user = Depends(validate_user_token)
):
    _result = decision_service.get_detail(decision_id=decision_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )

# API Create ------------------------------------------------------------------------------------------------------
@decision_router.post(path="/decision/")
@try_catch
async def create(
    request: Request,
    data: DecisionCreateDTO = Body(...),
    images: List[UploadFile] = Depends(ValidationHelper.validate_list_image),
    files: List[UploadFile] = Depends(ValidationHelper.validate_list_pdf),
    commitments: List[UploadFile] = Depends(ValidationHelper.validate_list_commitments),
    petitions: List[UploadFile] = Depends(ValidationHelper.validate_list_petition),
    user = Depends(validate_user_token)
):
    _result = decision_service.create(
        decision=data,
        images=images,
        files=files,
        commitments=commitments,
        petitions=petitions,
        username=user
    )

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


@decision_router.get(path="/decision/{decision_id}/image/{image_id}/{type_image}")
@try_catch
async def get_image_content(
    request: Request,
    decision_id: str = None,
    image_id: str = None,
    type_image: str = 'original',
    user = Depends(validate_user_token)
):
    folder_path = './data/decision'

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


@decision_router.get(path="/decision/{decision_id}/file/{file_id}")
@try_catch
async def get_file_content(
    request: Request,
    decision_id: str = None,
    file_id: str = None,
    user = Depends(validate_user_token)
):
    folder_path = './data/decision'

    with open(f'{folder_path}/{file_id}.enc', 'rb') as enc_file:
        enc_data = enc_file.read()

    decrypted_data = AESHelper.decrypt_image(enc_data)

    import io
    return StreamingResponse(
        io.BytesIO(decrypted_data),
        media_type='application/pdf'
    )


#API Update ------------------------------------------------------------------------------------------------------
@decision_router.put(path="/decision/{decision_id}")
@try_catch
async def update(
    request: Request,
    decision_id: str = None,
    data: DecisionUpdateDTO = Body(...),
    images: List[UploadFile] = Depends(ValidationHelper.validate_list_image),
    files: List[UploadFile] = Depends(ValidationHelper.validate_list_pdf),
    commitments: List[UploadFile] = Depends(ValidationHelper.validate_list_commitments),
    petitions: List[UploadFile] = Depends(ValidationHelper.validate_list_petition),
    user = Depends(validate_user_token)
):
    decision_service.get_detail(decision_id=decision_id)

    _result = decision_service.update(
        decision_id=decision_id,
        decision=data,
        images=images,
        files=files,
        commitments=commitments,
        petitions=petitions,
        username=user
    )

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


#API Remove ------------------------------------------------------------------------------------------------------
@decision_router.delete(path="/decision/{decision_id}")
@try_catch
async def remove(
    request: Request,
    decision_id: str = None,
    user = Depends(validate_user_token)
):
    decision_service.get_detail(decision_id=decision_id)

    _result = decision_service.remove(decision_id=decision_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )
