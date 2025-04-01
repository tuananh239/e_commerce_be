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
from app.libs.helpers.time_helper import MILISECOND, TimeHelper
from app.libs.helpers.validation_helper import ValidationHelper
from app.src.dependencies.auth_dependency import validate_user_token
from app.src.models.dto.order_dto import OrderDTO, OrderCreateDTO, OrderUpdateDTO, OrderGetDTO
from app.src.models.dto.user_dto import UserPaidDTO
from app.src.services.order_service import OrderService
from app.src.services.user_service import UserService

# =================================================================================================================

# Declare Element =================================================================================================

# Main ============================================================================================================

order_router = get_router()

order_controller = Controller(
    router=order_router,
    tags=["Order"]
)

order_service = OrderService()
user_service = UserService()

# Implement API ===================================================================================================
# API Get ---------------------------------------------------------------------------------------------------------
@order_router.get(path="/order")
@try_catch
async def get_list(
    request: Request,
    params: OrderGetDTO = Depends(),
    user = Depends(validate_user_token)
):
    _result, _pagination, _sort = order_service.get(params=params, user=user)

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
    user = Depends(validate_user_token)
):
    _result = order_service.get_detail(order_id=order_id, user=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )

# API Create ------------------------------------------------------------------------------------------------------
@order_router.post(path="/order")
@try_catch
async def create(
    request: Request,
    data: OrderCreateDTO = Body(...),
    image: UploadFile = Depends(ValidationHelper.validate_image),
    user = Depends(validate_user_token)
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
    user = Depends(validate_user_token)
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
    user = Depends(validate_user_token)
):
    order_service.get_detail(order_id=order_id, user=user)

    _result = order_service.update(order_id=order_id, order=data, images=images, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


@order_router.put(path="/order/{order_id}/paid")
@try_catch
async def paid(
    request: Request,
    order_id: str = None,
    user_paid: UserPaidDTO = Body(...),
    user = Depends(validate_user_token)
):
    order_detail = order_service.get_detail(order_id=order_id, user=user)

    user_service.paid(email=user, user_amount=user_paid.amount)

    order_detail.total_paid = user_paid.amount
    order_detail.status = 3
    order_detail.deposit_at = TimeHelper.get_timestamp_now(level=MILISECOND)

    _result = order_service.update(order_id=order_id, order=order_detail, images=[], username=user)

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
    order_service.get_detail(order_id=order_id, user=user)

    _result = order_service.remove(order_id=order_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )
