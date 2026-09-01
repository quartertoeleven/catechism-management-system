from typing import Optional, Tuple

from cms_integrations.logto import SIGN_IN_SESSION_KEY, LogtoClientFactory, LogtoService
from fastapi import Request
from fastapi.responses import RedirectResponse
from logto import IdTokenClaims, LogtoClient

from services.session_storage import FastAPISessionCookieStorage


class AuthService:
    def __init__(
        self,
        logto_client_factory: LogtoClientFactory,
        logto_service: LogtoService,
        logto_redirect_uri: str,
        frontend_url: str,
        session_secret: str,
        cookie_name: str,
        cookie_secure: bool,
        cookie_samesite: str,
        cookie_max_age: int,
    ) -> None:
        self._logto_client_factory = logto_client_factory
        self._logto_service = logto_service
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
    ) -> Tuple[LogtoClient, FastAPISessionCookieStorage]:
        storage = FastAPISessionCookieStorage.from_request(
            request, *self._cookie_params
        )
        return self._logto_client_factory.create_client(storage), storage

    def create_client(self, request: Request) -> LogtoClient:
        client, _ = self._client_with_storage(request)
        return client

    async def build_sign_in_url(self, request: Request) -> RedirectResponse:
        client, storage = self._client_with_storage(request)
        sign_in_url = await self._logto_service.build_sign_in_url(
            client, self._logto_redirect_uri
        )
        response = RedirectResponse(sign_in_url, status_code=302)
        storage.write_to(response)
        return response

    async def handle_sign_in_callback(
        self, request: Request, callback_url: str
    ) -> RedirectResponse:
        client, storage = self._client_with_storage(request)
        await self._logto_service.handle_sign_in_callback(client, callback_url)
        response = RedirectResponse(self._frontend_url, status_code=302)
        storage.write_to(response)
        return response

    async def build_sign_out_url(self, request: Request) -> RedirectResponse:
        client, storage = self._client_with_storage(request)
        storage.delete(SIGN_IN_SESSION_KEY)
        sign_out_url = await self._logto_service.build_sign_out_url(
            client, self._frontend_url
        )
        response = RedirectResponse(sign_out_url, status_code=302)
        storage.write_to(response)
        return response

    async def get_current_user(self, request: Request) -> Optional[IdTokenClaims]:
        client, _ = self._client_with_storage(request)
        return await self._logto_service.get_claims(client)
