# ===========================================================================================
# Fast API Route
# Dev: anh.vu
# ===========================================================================================

"""
    Cấu hình riêng cho fastapi app. Các thành phần:
"""

# ===========================================================================================

from typing import Callable
from fastapi.encoders import jsonable_encoder

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.routing import APIRoute

from app.libs.exception.exceptions import handle_exception

# ===========================================================================================

class ExceptionRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                response: Response = await original_route_handler(request)
                return response
            except Exception as e:
                return handle_exception(request, e)

        return custom_route_handler

# Main ======================================================================================
def get_router():
    return APIRouter(route_class=ExceptionRoute)

class Controller():
    def __init__(self, router, tags) -> None:
        self.router = router
        self.tags = tags