# ===========================================================================================
# JWT Config
# Dev: anh.vu
# ===========================================================================================

"""
    * Chứa tất cả các cấu hình các loại Bearer Authentication
"""

# ===========================================================================================

from pydantic import BaseModel

# ===========================================================================================

class JWTOptions():
    def __init__(
            self,
            verify_signature: bool = True,
            verify_exp: bool = True,
            verify_nbf: bool = True,
            verify_iat: bool = True,
            verify_aud: bool = True,
            verify_iss: bool = True,
            require_exp: bool = False,
            require_iat: bool = False,
            require_nbf: bool = False,
            ) -> None:
        self.verify_signature = verify_signature
        self.verify_exp = verify_exp
        self.verify_nbf = verify_nbf
        self.verify_iat = verify_iat
        self.verify_aud = verify_aud
        self.verify_iss = verify_iss
        self.require_exp = require_exp
        self.require_iat = require_iat
        self.require_nbf = require_nbf
    

class JWTBearerConfig():
    def __init__(self, name: str, public_key: str, options: dict) -> None:
        self.name = name
        self.public_key = public_key
        self.options = options

