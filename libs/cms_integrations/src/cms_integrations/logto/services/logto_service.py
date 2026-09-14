import logging
from typing import Optional, Tuple

from logto import IdTokenClaims, LogtoClient, UserInfoResponse

from cms_integrations.logto.services.jwt_verification_service import (
    JwtVerificationService,
    TokenExpiredError,
)

logger = logging.getLogger(__name__)


class LogtoService:
    def __init__(self, jwt_verification_service: JwtVerificationService) -> None:
        self._jwt_verification_service = jwt_verification_service

    async def build_sign_in_url(self, client: LogtoClient, redirect_uri: str) -> str:
        return await client.signIn(redirect_uri)

    async def handle_sign_in_callback(
        self, client: LogtoClient, callback_url: str
    ) -> None:
        await client.handleSignInCallback(callback_url)

    async def build_sign_out_url(
        self, client: LogtoClient, post_logout_redirect_uri: str
    ) -> str:
        return await client.signOut(post_logout_redirect_uri)

    async def get_user_info(self, client: LogtoClient) -> UserInfoResponse:
        return await client.fetchUserInfo()

    def get_raw_id_token(self, client: LogtoClient) -> Optional[str]:
        return client._storage.get("idToken")

    async def get_claims(self, client: LogtoClient) -> Tuple[Optional[IdTokenClaims], bool]:
        if not client.isAuthenticated():
            return None, False

        raw_token = self.get_raw_id_token(client)
        if raw_token is None:
            return None, False

        try:
            return await self._jwt_verification_service.verify(raw_token), False
        except TokenExpiredError:
            logger.info("ID token expired, attempting refresh")

        try:
            await client.getAccessToken()
        except Exception:
            logger.exception("Token refresh failed")
            return None, False

        new_raw_token = self.get_raw_id_token(client)
        if new_raw_token is None:
            logger.warning("Token refresh succeeded but no ID token in storage")
            return None, False

        try:
            claims = await self._jwt_verification_service.verify(new_raw_token)
        except TokenExpiredError:
            return None, False

        logger.info("Token refresh succeeded")
        return claims, True
