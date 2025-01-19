# ===========================================================================================
# Response model
# Dev: anh.vu
# ===========================================================================================

import json
import uuid
from starlette import status
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.libs.exception.soa_error import SOA

# ===========================================================================================

# Sub class =================================================================================


# Main class ================================================================================
class BaseResponse():
    """
        Định nghĩa tất cả các trường cần có trong response
    """
    def __init__(self,
                 path,
                 client_message_id=str(uuid.uuid4()),
                 data=None,
                 http_status=status.HTTP_200_OK,
                 error="",
                 soa_error_code=SOA.SUCCESS.code,
                 soa_error_desc=SOA.SUCCESS.description) -> None:
        self.client_message_id = client_message_id if client_message_id else str(uuid.uuid4())
        self.data = data if data else {"result": None}
        self.status = http_status
        self.error = error
        self.soa_error_code = soa_error_code
        self.soa_error_desc = soa_error_desc
        self.path = path

    def json(self):
        json_response = JSONResponse(status_code=self.status, content=jsonable_encoder(self.__dict__))
        _headers = json_response.headers.mutablecopy()
        _headers.update({"Access-Control-Allow-Origin": "*", "client-message-id": self.client_message_id})

        return JSONResponse(status_code=self.status, content=jsonable_encoder(self.__dict__), headers=_headers)


class ResponseSuccess(BaseResponse):
    """
        Format response trả về khi xử lý thành công.
    """
    def __init__(self, client_message_id=uuid.uuid4(), path="", result={}, pagination=None, sort=None, http_status=status.HTTP_200_OK) -> None:
        super().__init__(
            client_message_id=client_message_id,
            path=path,
            data=self._create_data(result=result, pagination=pagination, sort=sort),
            http_status=http_status
        )

    
    def _create_data(self, result, pagination, sort):
        if pagination is not None and sort is not None:
            sort.sort = "asc" if sort.sort == 1 or sort.sort == "asc" else "desc"
            return {
                "result": result,
                "pagination": pagination,
                "sort": sort
            }
        else:
            return{
                "result": result
            }
        
    
class ResponseError(BaseResponse):
    """
        Format response trả về khi xử lý gặp lỗi.
    """
    def __init__(self,
                 client_message_id,
                 path,
                 http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                 error="System error.",
                 soa_error_code=SOA.SYSTEM_ERROR.code,
                 soa_error_desc=SOA.SYSTEM_ERROR.description) -> None:
        super().__init__(
            client_message_id=client_message_id,
            path=path,
            http_status=http_status,
            error=error,
            soa_error_code=soa_error_code,
            soa_error_desc=soa_error_desc
        )