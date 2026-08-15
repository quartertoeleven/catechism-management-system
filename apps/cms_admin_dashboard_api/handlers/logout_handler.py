from fastapi import Request
from fastapi.responses import RedirectResponse

from services.auth_service import AuthService


class LogoutHandler:
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    async def build_sign_out_url(self, request: Request) -> RedirectResponse:
        return await self._auth_service.build_sign_out_url(request)
