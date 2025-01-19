# =================================================================================================================
# Feature: oder_controller
# =================================================================================================================

"""
    Định nghĩa và triển khai tất cả các API liên quan đến Order
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
from app.src.models.dto.order_dto import OrderDTO, OrderCreateDTO, OrderUpdateDTO, OrderGetDTO
from app.src.services.order_service import OrderService

# =================================================================================================================

# Declare Element =================================================================================================

# Main ============================================================================================================

order_router = get_router()

order_controller = Controller(
    router=order_router,
    tags=["Order"]
)

order_service = OrderService()

# Implement API ===================================================================================================
# API Get ---------------------------------------------------------------------------------------------------------
@order_router.get(path="/order/")
@try_catch
async def get_list(
    request: Request,
    params: OrderGetDTO = Depends(),
    # user = Depends(validate_user_token)
):
    _result, _pagination, _sort = order_service.get(params=params)

    return ResponseSuccess(
        path=request.url.path,
        result=_result,
        pagination=_pagination,
        sort=_sort
    )


# API Get detail by transaction -----------------------------------------------------------------------------------
@order_router.get(path="/order/{order_id}")
@try_catch
async def get_detail(
    request: Request,
    order_id: str = None,
    # user = Depends(validate_user_token)
):
    _result = order_service.get_detail(order_id=order_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )

# API Create ------------------------------------------------------------------------------------------------------
@order_router.post(path="/order/")
@try_catch
async def create(
    request: Request,
    data: OrderCreateDTO = Body(...),
    image: UploadFile = Depends(ValidationHelper.validate_image),
    # user = Depends(validate_user_token)
    user = "user"
):

    _result = order_service.create(order=data, image=image, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


@order_router.get(path="/order/{order_id}/image/{image_id}/{type_image}")
@try_catch
async def get_image_content(
    request: Request,
    order_id: str = None,
    image_id: str = None,
    type_image: str = 'original',
    # user = Depends(validate_user_token)
    user = "user"
):
    folder_path = './data/order'
    
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


#API Update ------------------------------------------------------------------------------------------------------
@order_router.put(path="/order/{order_id}")
@try_catch
async def update(
    request: Request,
    order_id: str = None,
    data: OrderUpdateDTO = Body(...),
    images: List[UploadFile] = Depends(ValidationHelper.validate_list_image),
    files: List[UploadFile] = Depends(ValidationHelper.validate_list_pdf),
    user = Depends(validate_user_token)
):
    order_service.get_detail(order_id=order_id)

    _result = order_service.update(order_id=order_id, order=data, images=images, files=files, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


#API Remove ------------------------------------------------------------------------------------------------------
@order_router.delete(path="/order/{order_id}")
@try_catch
async def remove(
    request: Request,
    order_id: str = None,
    user = Depends(validate_user_token)
):
    order_service.get_detail(order_id=order_id)

    _result = order_service.remove(order_id=order_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )
