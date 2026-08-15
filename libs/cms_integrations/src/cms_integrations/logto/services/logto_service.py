import time
from typing import Optional

from logto import IdTokenClaims, LogtoClient, UserInfoResponse


class LogtoService:
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