from fastapi import Request
from fastapi.responses import RedirectResponse
from handlers.base_handler import BaseAsyncHandler
from services.auth_service import AuthService


class LoginHandler(BaseAsyncHandler):
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    async def handle(self, request: Request) -> RedirectResponse:
        return await self._auth_service.build_sign_in_url(request)
