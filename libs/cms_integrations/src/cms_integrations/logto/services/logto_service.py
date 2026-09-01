from typing import Optional

from logto import IdTokenClaims, LogtoClient, UserInfoResponse


class LogtoService:
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

    async def verify_id_token(self, client: LogtoClient, raw_token: str) -> None:
        oidc_core = await client.getOidcCore()
        oidc_core.verifyIdToken(raw_token, client.config.appId)

    async def get_claims(self, client: LogtoClient) -> Optional[IdTokenClaims]:
        if not client.isAuthenticated():
            return None
        raw_token = self.get_raw_id_token(client)
        if raw_token is None:
            return None
        try:
            await self.verify_id_token(client, raw_token)
        except Exception:
            return None
        return client.getIdTokenClaims()
