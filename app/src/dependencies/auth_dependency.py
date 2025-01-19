# =================================================================================================================
# Feature: auth_dependency
# Dev: anhvt9
# Start Date: 28/04/2023
# Maintain Date: 27/04/2023
# =================================================================================================================

"""
    Hỗ trợ việc phân quyền cho tất cả các API
"""

# =================================================================================================================

from fastapi import Depends, Request
from fastapi.security import HTTPBearer

from app.libs.authentication.bearer_auth import verify_token
from app.libs.exception.exceptions import AuthorizationException
from app.libs.exception.soa_error import SOA

from app.src.commons.constants.constants import JWT_CONST

# =================================================================================================================

def _get_user_keycloak(payload: dict):
    """
        Get user infor of Keycloak
    :param payload:
    :return:
    """
    if 'preferred_username' in payload.keys():
        return payload['preferred_username']
    else:
        raise AuthorizationException(
            message="Invalid token - Detail: 'preferred_username' not in payload."
        )

def validate_user_token(request: Request,
                        http_authorization_credentials=Depends(HTTPBearer())
                        ):
    """"""
    _token = http_authorization_credentials.credentials

    _payload = verify_token(
        token=_token,
        jwt_config=JWT_CONST.KEYCLOAK_INTERNAL
    )

    _user = _get_user_keycloak(_payload)

    return _user


def validate_token(request: Request):
    """"""
    if "OcrFedAuth" not in request.cookies:
        raise AuthorizationException(message=f"Token invalid! - Detail: 'OcrFedAuth' not in cookie.")
    _token = request.cookies.get("OcrFedAuth")

    return _token


