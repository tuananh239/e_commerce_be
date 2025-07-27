# =================================================================================================================
# Feature: cart_controller
# =================================================================================================================

"""
    Định nghĩa và triển khai tất cả các API liên quan đến Cart
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
from app.src.models.dto.cart_dto import CartDTO, CartUpdateDTO
from app.src.models.dto.order_dto import ProductDTO
from app.src.models.dto.user_dto import UserPaidDTO
from app.src.services.cart_service import CartService
from app.src.services.user_service import UserService

# =================================================================================================================

# Declare Element =================================================================================================

# Main ============================================================================================================

cart_router = get_router()

cart_controller = Controller(
    router=cart_router,
    tags=["Cart"]
)

cart_service = CartService()
user_service = UserService()

# Implement API ===================================================================================================
# API Get ---------------------------------------------------------------------------------------------------------
@cart_router.get(path="/cart")
@try_catch
async def get(
    request: Request,
    user = Depends(validate_user_token)
):
    _result = cart_service.get(username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


# API Create ------------------------------------------------------------------------------------------------------
@cart_router.post(path="/cart/add-product")
@try_catch
async def create(
    request: Request,
    data: ProductDTO = Body(...),
    user = Depends(validate_user_token)
):

    _result = cart_service.add_product(product=data, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )


@cart_router.put(path="/cart/{cart_id}")
@try_catch
async def update(
    request: Request,
    cart_id: str = None,
    data: CartUpdateDTO = Body(...),
    user = Depends(validate_user_token)
):

    _result = cart_service.update(cart_id=cart_id, card=data, username=user)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )

#API Remove ------------------------------------------------------------------------------------------------------
@cart_router.delete(path="/cart/{cart_id}")
@try_catch
async def remove(
    request: Request,
    cart_id: str = None,
    user = Depends(validate_user_token)
):
    cart_service.get_detail(cart_id=cart_id, user=user)

    _result = cart_service.remove(cart_id=cart_id)

    return ResponseSuccess(
        path=request.url.path,
        result=_result
    )
