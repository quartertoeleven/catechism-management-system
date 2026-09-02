import logging
from typing import Optional

import jwt
from jwt import PyJWKClient
from logto import IdTokenClaims

logger = logging.getLogger(__name__)


class JwtVerificationService:
    def __init__(self, endpoint: str, app_id: str) -> None:
        self._endpoint = endpoint.rstrip("/") + "/oidc"
        self._app_id = app_id
        self._jwks_client = PyJWKClient(
            f"{self._endpoint}/oidc/jwks",
            cache_jwk_set=True,
            cache_keys=False,
        )

    async def verify(self, raw_token: str) -> Optional[IdTokenClaims]:
        try:
            signing_key = self._jwks_client.get_signing_key_from_jwt(raw_token)
            payload = jwt.decode(
                raw_token,
                signing_key.key,
                algorithms=["RS256", "PS256", "ES256", "ES384", "ES512"],
                audience=self._app_id,
                issuer=self._endpoint,
                leeway=30,
                options={
                    "require": ["exp", "iss", "aud", "sub", "iat"],
                },
            )
            return IdTokenClaims(**payload)
        except (jwt.InvalidTokenError, jwt.PyJWKClientError) as e:
            logger.exception("JWT verification failed: %s", e)
            return None
