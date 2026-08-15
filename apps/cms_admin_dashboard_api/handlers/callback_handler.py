from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from logto import LogtoException

from services.auth_service import AuthService


class CallbackHandler:
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    async def handle_sign_in_callback(self, request: Request) -> RedirectResponse:
        try:
            return await self._auth_service.handle_sign_in_callback(
                request, str(request.url)
            )
        except LogtoException as exc:
            raise HTTPException(
                status_code=400, detail=f"Sign-in callback failed: {exc}"
            )
