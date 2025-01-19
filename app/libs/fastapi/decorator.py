# ===========================================================================================
# Decorator Controller
# Dev: anh.vu
# ===========================================================================================

"""
    Các decorator phục vụ cho việc viết API. Các thành phần:
        - Try catch
"""

# ===========================================================================================
import uuid
from functools import wraps
from pydantic import ValidationError
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette import status

from app.libs.fastapi.response import ResponseSuccess, ResponseError
from app.libs.exception.soa_error import SOA
from app.libs.exception.exceptions import (
    AuthorizationException, NotFoundException, ValidationException, RepositoryException, NotAllowedException
)

# Main ======================================================================================

def try_catch(handler):
    @wraps(handler)
    async def wrapper(request: Request, client_message_id=None, *args, **kwargs):
        _response = None

        try:
            if client_message_id:
                _controller_response = await handler(request, client_message_id, *args, **kwargs)
            else:
                _controller_response = await handler(request, *args, **kwargs)
            if isinstance(_controller_response, ResponseSuccess):
                _response = ResponseSuccess(
                    client_message_id=client_message_id,
                    path=request.url.path,
                    http_status=_controller_response.status,
                    result=_controller_response.data.get('result'),
                    pagination=_controller_response.data.get('pagination'),
                    sort=_controller_response.data.get('sort')
                )
                return _response.json()
            else:
                return _controller_response
        except (
            NotFoundException,
            NotAllowedException,
            ValidationException,
            RepositoryException,
            AuthorizationException
            ) as e:
            _response = ResponseError(
                client_message_id=client_message_id,
                path=request.url.path,
                http_status=e.status_code,
                error=e.message,
                soa_error_code=e.soa_error_code,
                soa_error_desc=e.soa_error_desc
            )

            return _response.json()
        except ValidationError as e:
            _response = ResponseError(
                client_message_id=client_message_id,
                path=request.url.path,
                http_status=status.HTTP_400_BAD_REQUEST,
                error=f'{e.__str__()}',
                soa_error_code=SOA.BAD_REQUEST.code,
                soa_error_desc=SOA.BAD_REQUEST.description
            )

            return _response.json()
        except Exception as e:
            _response = ResponseError(
                client_message_id=client_message_id,
                path=request.url.path,
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error=f'{e.__str__()}',
                soa_error_code=SOA.SYSTEM_ERROR.code,
                soa_error_desc=SOA.SYSTEM_ERROR.description
            )

            return _response.json()

    return wrapper