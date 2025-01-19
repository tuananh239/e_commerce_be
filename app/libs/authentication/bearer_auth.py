# ===========================================================================================
# Bearer Authentication
# Dev: anh.vu
# ===========================================================================================

"""
    * Chứa tất cả các phương thức hỗ trợ cho Bearer Authentication
"""

# ===========================================================================================

from app.libs.exception.soa_error import SOA
import jwt

from app.libs.exception.exceptions import AuthorizationException
from app.libs.authentication.jwt_config import JWTBearerConfig

# ===========================================================================================

def verify_token(token, jwt_config: JWTBearerConfig):
    """
        Kiểm tra xem token có hợp lệ hay không
        jwt_config_name: tên của loại jwt đang sử dụng
        list_jwt_config: danh sách các loại token đang được sử dụng trong hệ thống
    """
    try:
        _, _, _header, _ = jwt.api_jws._jws_global_obj._load(token)

        return jwt.decode(
            jwt=token,
            key=jwt_config.public_key,
            options=jwt_config.options.__dict__,
            algorithms=[_header.get('alg')]
        )
    except (
        jwt.DecodeError,
        jwt.ImmatureSignatureError,
        jwt.InvalidAudienceError,
        jwt.InvalidIssuedAtError,
        jwt.InvalidIssuerError,
        jwt.MissingRequiredClaimError,
        ) as e:
        raise AuthorizationException(
            message=f"Invalid token - {e.__str__()}"
        )
    except jwt.ExpiredSignatureError as e:
        raise AuthorizationException(
            message=f"Expired token - {e.__str__()}"
        )
    except Exception as e:
        raise AuthorizationException(
            message=f"Auth error - {e.__str__()}"
        )
