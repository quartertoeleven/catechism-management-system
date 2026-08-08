import time
from typing import Optional, Tuple

from fastapi import Request
from fastapi.responses import RedirectResponse
from logto import IdTokenClaims, LogtoClient, LogtoConfig

from services.session_storage import SessionCookieStorage


class AuthService:
    def __init__(
        self,
        logto_endpoint: str,
        logto_app_id: str,
        logto_app_secret: str,
        logto_redirect_uri: str,
        frontend_url: str,
        session_secret: str,
        cookie_name: str,
        cookie_secure: bool,
        cookie_samesite: str,
        cookie_max_age: int,
    ) -> None:
        self._logto_config = LogtoConfig(
            endpoint=logto_endpoint,
            appId=logto_app_id,
            appSecret=logto_app_secret,
        )
        self._logto_redirect_uri = logto_redirect_uri
        self._frontend_url = frontend_url
        self._cookie_params = (
            session_secret,
            cookie_name,
            cookie_secure,
            cookie_samesite,
            cookie_max_age,
        )

    def _client_with_storage(
        self, request: Request
    ) -> Tuple[LogtoClient, SessionCookieStorage]:
        storage = SessionCookieStorage.from_request(request, *self._cookie_params)
        return LogtoClient(self._logto_config, storage), storage

    async def build_sign_in_url(self, request: Request) -> RedirectResponse:
        client, storage = self._client_with_storage(request)
        sign_in_url = await client.signIn(self._logto_redirect_uri)
        response = RedirectResponse(sign_in_url, status_code=302)
        storage.write_to(response)
        return response

    async def handle_sign_in_callback(
        self, request: Request, callback_url: str
    ) -> RedirectResponse:
        client, storage = self._client_with_storage(request)
        await client.handleSignInCallback(callback_url)
        response = RedirectResponse(self._frontend_url, status_code=302)
        storage.write_to(response)
        return response

    async def build_sign_out_url(self, request: Request) -> RedirectResponse:
        client, storage = self._client_with_storage(request)
        storage.delete("signInSession")
        sign_out_url = await client.signOut(self._frontend_url)
        response = RedirectResponse(sign_out_url, status_code=302)
        storage.write_to(response)
        return response

    def get_current_user(self, request: Request) -> Optional[IdTokenClaims]:
        client, _ = self._client_with_storage(request)
        if not client.isAuthenticated():
            return None
        claims = client.getIdTokenClaims()
        if claims.exp < int(time.time()):
            return None
        return claims
