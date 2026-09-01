from cms_locale import Translator
from fastapi import HTTPException, Request
from handlers.base_handler import BaseAsyncHandler
from models.check_response import CheckResponse
from services.auth_service import AuthService


class CheckHandler(BaseAsyncHandler):
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    async def handle(self, request: Request, translator: Translator) -> CheckResponse:
        claims = await self._auth_service.get_current_user(request)
        if claims is None:
            raise HTTPException(
                status_code=401,
                detail=translator.gettext("error.not_authenticated"),
            )
        return CheckResponse(authenticated=True, sub=claims.sub)
