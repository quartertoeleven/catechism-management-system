import time
from typing import Optional

from logto import (
    IdTokenClaims,
    LogtoClient,
    LogtoConfig,
    Scope,
    UserInfoResponse,
    UserInfoScope,
)
from logto.Storage import Storage

DEFAULT_SCOPES: list[Scope] = [
    UserInfoScope.openid,
    UserInfoScope.email,
    UserInfoScope.custom_data,
]


class LogtoAuthClient:
    def __init__(
        self,
        endpoint: str,
        app_id: str,
        app_secret: str,
        scopes: Optional[list[Scope]] = None,
    ) -> None:
        self._config = LogtoConfig(
            endpoint=endpoint,
            appId=app_id,
            appSecret=app_secret,
            scopes=list(scopes if scopes is not None else DEFAULT_SCOPES),
        )

    def create_client(self, storage: Storage) -> LogtoClient:
        return LogtoClient(self._config, storage)

    async def build_sign_in_url(
        self, client: LogtoClient, redirect_uri: str
    ) -> str:
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

    def get_claims(self, client: LogtoClient) -> Optional[IdTokenClaims]:
        if not client.isAuthenticated():
            return None
        claims = client.getIdTokenClaims()
        if claims.exp < int(time.time()):
            return None
        return claims