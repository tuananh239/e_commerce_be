# ===========================================================================================
# Exceptions
# Dev: anh.vu
# ===========================================================================================

"""
    * Mô tả tất cả các Exception có thể xảy ra
"""
# ===========================================================================================

from fastapi import Request
from starlette import status
from fastapi.exceptions import(
    RequestValidationError, HTTPException, FastAPIError, WebSocketRequestValidationError
)

from app.libs.fastapi.response import ResponseError
from app.libs.exception.soa_error import SOA


# Main class ================================================================================
class NotFoundException(Exception):
    """
        Sử dụng khi gặp lỗi không tìm thấy kết quả
    """

    def __init__(self, status_code: int = 404, message: str = "Not found!", soa_error_code: str = SOA.NOT_FOUND.code, soa_error_desc: str = SOA.NOT_FOUND.description) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.soa_error_code = soa_error_code
        self.soa_error_desc = soa_error_desc


class NotAllowedException(Exception):
    """
        Sử dụng khi gặp lỗi không không được phép
    """

    def __init__(self, status_code: int = 405, message: str = "Not allowed!", soa_error_code: str = SOA.NOT_ALLOWED.code, soa_error_desc: str = SOA.NOT_ALLOWED.description) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.soa_error_code = soa_error_code
        self.soa_error_desc = soa_error_desc


class ValidationException(Exception):
    """
        Sử dụng khi gặp lỗi thông tin dữ liệu không hợp lệ
    """

    def __init__(self, status_code: str = 400, message: str = "Validation error!", soa_error_code: str = SOA.BAD_REQUEST.code, soa_error_desc: str = SOA.BAD_REQUEST.description) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.soa_error_code = soa_error_code
        self.soa_error_desc = soa_error_desc


class RepositoryException(Exception):
    """
        Sử dụng khi gặp lỗi cập nhật thông tin database
    """

    def __init__(self, status_code: str = 500, message: str = "Reposiroty error!", soa_error_code: str = SOA.BAD_REQUEST.code, soa_error_desc: str = SOA.BAD_REQUEST.description) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.soa_error_code = soa_error_code
        self.soa_error_desc = soa_error_desc


class ForbiddenException(Exception):
    """
        Sử dụng khi gặp lỗi cập nhật thông tin database
    """

    def __init__(self, status_code: str = 403, message: str = "Forbidden!", soa_error_code: str = SOA.FORBIDDEN.code, soa_error_desc: str = SOA.FORBIDDEN.description) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.soa_error_code = soa_error_code
        self.soa_error_desc = soa_error_desc


class AuthorizationException(Exception):
    """
        Sử dụng khi gặp lỗi cập nhật thông tin database
    """

    def __init__(self, status_code: str = 401, message: str = "Unauthorized!", soa_error_code: str = SOA.UNAUTHORIZED.code, soa_error_desc: str = SOA.UNAUTHORIZED.description) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.soa_error_code = soa_error_code
        self.soa_error_desc = soa_error_desc


# ===========================================================================================

# Xử lý tất cả các exception đã được định nghĩa
def handle_exception(request: Request, exc):
    client_message_id = request.headers.get("client_message_id")
    if isinstance(exc, NotFoundException) \
            or isinstance(exc, ValidationException) \
            or isinstance(exc, NotAllowedException) \
            or isinstance(exc, RepositoryException) \
            or isinstance(exc, AuthorizationException) \
            or isinstance(exc, ForbiddenException):
        return ResponseError(
            client_message_id=client_message_id,
            path=request.url.path,
            http_status=exc.status_code,
            error=f"{exc.message}",
            soa_error_code=exc.soa_error_code,
            soa_error_desc=exc.soa_error_desc
        ).json()
    elif isinstance(exc, HTTPException):
        return ResponseError(
            client_message_id=client_message_id,
            path=request.url.path,
            http_status=exc.status_code,
            error=f"{exc.detail}",
            soa_error_code=SOA.FAST_API.code,
            soa_error_desc=SOA.FAST_API.description
        ).json()
    elif isinstance(exc, RequestValidationError):
        list_field_error = []
        for error in exc.errors():
            _field = ".".join([str(loc) for loc in error['loc']])
            list_field_error.append(f"{_field} is {error['msg']}")

        return ResponseError(
            client_message_id=client_message_id,
            path=request.url.path,
            http_status=status.HTTP_400_BAD_REQUEST,
            error=', '.join(list_field_error),
            soa_error_code=SOA.BAD_REQUEST.code,
            soa_error_desc=SOA.BAD_REQUEST.description
        ).json()
    elif isinstance(exc, FastAPIError):
        return ResponseError(
            client_message_id=client_message_id,
            path=request.url.path,
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="Runtime Error",
            soa_error_code=SOA.FAST_API.code,
            soa_error_desc=SOA.FAST_API.description
        ).json()
    elif isinstance(exc, WebSocketRequestValidationError):
        return ResponseError(
            client_message_id=client_message_id,
            path=request.url.path,
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="Websocket Error",
            soa_error_code=SOA.FAST_API.code,
            soa_error_desc=SOA.FAST_API.description
        ).json()
    else:
        return ResponseError(
            client_message_id=client_message_id,
            path=request.url.path,
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=f"{exc.__str__()}",
            soa_error_code=SOA.SYSTEM_ERROR.code,
            soa_error_desc=SOA.SYSTEM_ERROR.description
        ).json()
