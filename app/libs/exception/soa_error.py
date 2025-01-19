# ===========================================================================================
# SOA Error
# Dev: anh.vu
# ===========================================================================================

"""
    Định nghĩa tất cả mã lỗi riêng biệt cho hệ thống
"""
# ===========================================================================================

from app.libs.pattern.creational.constant import Constant

# ===========================================================================================

PREFIX_SOA_CODE = "EC"

# Sub class =================================================================================
class SoaError():
    def __init__(self, code: str = "", description: str = "") -> None:
        self.code = code
        self.description = description

class SoaErrorConst(Constant):
    """
        Mô tả tất cả các lỗi đặc thù của OCR Business Analyst
    """
    FAST_API = SoaError(
        code=f"{PREFIX_SOA_CODE}_FA_0001",
        description="Fast API - Error."
    )
    SUCCESS = SoaError(
        code=f"{PREFIX_SOA_CODE}_OK_0000",
        description="Success."
    )
    UNAUTHORIZED = SoaError(
        code=f"{PREFIX_SOA_CODE}_RQ_0001",
        description="Request error - Unauthorized."
    )
    BAD_REQUEST = SoaError(
        code=f"{PREFIX_SOA_CODE}_RQ_0002",
        description="Request error - Bad request."
    )
    NOT_FOUND = SoaError(
        code=f"{PREFIX_SOA_CODE}_RQ_0003",
        description="Request error - Data not found."
    )
    SYSTEM_ERROR = SoaError(
        code=f"{PREFIX_SOA_CODE}_SY_0004",
        description="System error."
    )
    REPOSITORY_ERROR = SoaError(
        code=f"{PREFIX_SOA_CODE}_RP_0005",
        description="Connection to database has problem."
    )
    NOT_ALLOWED = SoaError(
        code=f"{PREFIX_SOA_CODE}_RQ_0006",
        description="Request error - Request was not allowed."
    )
    FORBIDDEN = SoaError(
        code=f"{PREFIX_SOA_CODE}_RQ_0007",
        description="Request error - Forbidden."
    )

    # Error code
    PAGE_NOT_EXIST = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0000")
    INPUT_TYPE_INVALID = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0001")
    INPUT_LENGTH_INVALID = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0002")
    INPUT_CONTENT_INVALID = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0003")
    INPUT_CONTENT_HTML = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0004")
    FILE_UPLOAD_INVALID = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0005")
    FILE_UPLOAD_SIZE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0006")
    BUSINESS_EXISTED = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0007")
    NOT_PERMISSION = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0008")
    CONNECT_DB = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0009")
    BUSINESS_NOT_FOUND = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0010")
    BUSINESS_REMOVE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0011")
    BUSINESS_REQUEST_UPDATE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0012")
    BUSINESS_CANCEL_UPDATE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0013")
    BUSINESS_APPROVE_UPDATE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0014")
    BUSINESS_REJECT_UPDATE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0015")
    BUSINESS_CHANGE_STEP = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0016")
    BUSINESS_CONFIG_INPUT = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0017")
    BUSINESS_CONFIG_OUTPUT = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0018")
    BUSINESS_CONFIG_REPORT = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0019")
    DOCUMENT_NOT_DONE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0020")
    DEV_REQUEST_NOT_CREATE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0021")
    DEV_REQUEST_NOT_APPROVE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0022")
    AVATAR_NOT_FOUND = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0023")
    DEV_REQUEST_NOT_FOUND = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0024")
    DEV_REQUEST_CANT_CREATE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0025")
    DEV_REQUEST_CANT_CREATE_NEW = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0026")
    DEV_REQUEST_CANT_CREATE_UPDATE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0027")
    ASSIGNEE_NOT_PERMISSION = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0028")
    DEV_REQUEST_CANT_SEND = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0029")
    DEV_REQUEST_CANT_CANCEL = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0030")
    DEV_REQUEST_CANT_APPROVE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0031")
    DEV_REQUEST_CANT_REJECT = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0032")
    TESTING_CANT_CREATE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0033")
    DATASET_NOT_EXISTED = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0034")
    BATCH_NOT_FOUND = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0035")
    DATASET_NOT_FOUND = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0036")
    BATCH_CONVERTING = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0037")
    BATCH_CONVERTED = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0038")
    DOCUMENT_NOT_FOUND = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0039")
    DOCTYPE_EXISTED = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0040")
    FILE_CONTAIN_JS = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0041")
    NO_BATCH_DATASET = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0042")
    NO_DATASET_IN_BATCH = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0043")
    DATASET_NOT_CONVERTED = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0044")
    NO_DOCUMENT_IN_BATCH = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0045")
    DOCUMENT_INVALID_IN_BATCH = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0046")
    DATASET_NOT_IN_DOCUMENT = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0047")
    BATCH_DATASET_NOT_DEVIDE = SoaError(code=f"{PREFIX_SOA_CODE}_ER_0048")

# Main class ================================================================================
SOA = SoaErrorConst()

