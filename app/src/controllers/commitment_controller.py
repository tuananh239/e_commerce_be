# =================================================================================================================
# Feature: commitment_controller
# =================================================================================================================

"""
    Định nghĩa và triển khai tất cả các API liên quan đến Commitment
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
from app.src.models.dto.commitment_dto import CommitmentCreateDTO, CommitmentDTO, CommitmentGetDTO, CommitmentUpdateDTO
from app.src.services.commitment_service import CommitmentService

# =================================================================================================================

# Declare Element =================================================================================================

# Main ============================================================================================================

commitment_router = get_router()

commitment_controller = Controller(
    router=commitment_router,
    tags=["Commitment"]
)

commitment_service = CommitmentService()

# Implement API ===================================================================================================
# API Get ---------------------------------------------------------------------------------------------------------
@commitment_router.get(path="/commitment/")
@try_catch
async def get_list(
    request: Request,
    params: CommitmentGetDTO = Depends(),
    user = Depends(validate_user_token)
):
    _result, _pagination, _sort = commitment_service.get(params=params)

    return ResponseSuccess(
        path=request.url.path,
        result=_result,
        pagination=_pagination,
        sort=_sort
    )


# API Get detail by transaction -----------------------------------------------------------------------------------
@commitment_router.get(path="/commitment/{commitment_id}")
@try_catch
async def get_detail(
    request: Request,
    commitment_id: str = None,
    user = Depends(validate_user_token)
):
    _result = commitment_service.get_detail(commitment_id=commitment_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )

# API Create ------------------------------------------------------------------------------------------------------
@commitment_router.post(path="/commitment/")
@try_catch
async def create(
    request: Request,
    data: CommitmentCreateDTO = Body(...),
    images: List[UploadFile] = Depends(ValidationHelper.validate_list_image),
    files: List[UploadFile] = Depends(ValidationHelper.validate_list_pdf),
    user = Depends(validate_user_token)
):
    _result = commitment_service.create(commitment=data, images=images, files=files, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )



@commitment_router.get(path="/commitment/{commitment_id}/image/{image_id}/{type_image}")
@try_catch
async def get_image_content(
    request: Request,
    commitment_id: str = None,
    image_id: str = None,
    type_image: str = 'original',
    user = Depends(validate_user_token)
):
    folder_path = './data/commitment'

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


@commitment_router.get(path="/commitment/{commitment_id}/file/{file_id}")
@try_catch
async def get_file_content(
    request: Request,
    commitment_id: str = None,
    file_id: str = None,
    user = Depends(validate_user_token)
):
    folder_path = './data/commitment'

    with open(f'{folder_path}/{file_id}.enc', 'rb') as enc_file:
        enc_data = enc_file.read()

    decrypted_data = AESHelper.decrypt_image(enc_data)

    import io
    return StreamingResponse(
        io.BytesIO(decrypted_data),
        media_type='application/pdf'
    )


#API Update ------------------------------------------------------------------------------------------------------
@commitment_router.put(path="/commitment/{commitment_id}")
@try_catch
async def update(
    request: Request,
    commitment_id: str = None,
    data: CommitmentUpdateDTO = Body(...),
    images: List[UploadFile] = Depends(ValidationHelper.validate_list_image),
    files: List[UploadFile] = Depends(ValidationHelper.validate_list_pdf),
    user = Depends(validate_user_token)
):
    commitment_service.get_detail(commitment_id=commitment_id)

    _result = commitment_service.update(commitment_id=commitment_id, commitment=data, images=images, files=files, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


#API Remove ------------------------------------------------------------------------------------------------------
@commitment_router.delete(path="/commitment/{commitment_id}")
@try_catch
async def remove(
    request: Request,
    commitment_id: str = None,
    user = Depends(validate_user_token)
):
    commitment_service.get_detail(commitment_id=commitment_id)

    _result = commitment_service.remove(commitment_id=commitment_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )
