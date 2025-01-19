# =================================================================================================================
# Feature: jwt_const
# Dev: anh.vu
# Start Date: 28/04/2023
# Maintain Date: 28/04/2023
# =================================================================================================================

from decouple import config
import decouple

from app.libs.pattern.creational.constant import Constant
from app.libs.pattern.creational.singleton import Singleton
from app.libs.authentication.jwt_config import JWTBearerConfig, JWTOptions

# Declear element =================================================================================================

# Sub class =======================================================================================================

class JWTInternal(JWTBearerConfig, Constant, metaclass=Singleton):
    """"""

# Main class ======================================================================================================

class JWTConstants(Constant, metaclass=Singleton):
    KEYCLOAK_INTERNAL = JWTBearerConfig(
        name="KEYCLOAK_INTERNAL",
        public_key=decouple.config('PUBLIC_KEY').replace("\\n", "\n"),
        options=JWTOptions(
            verify_signature = True,
            verify_exp = True,
            verify_nbf = True,
            verify_iat = False,
            verify_aud = False,
            verify_iss = False,
            require_exp = True,
            require_iat = False,
            require_nbf = False,
        )
    )

    LIST = [
        KEYCLOAK_INTERNAL
    ]

    PRIVATE_KEY = decouple.config('PRIVATE_KEY').replace("\\n", "\n")
    PUBLIC_KEY = decouple.config('PUBLIC_KEY').replace("\\n", "\n")

