from cms_locale import Translator
from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse
from handlers.base_handler import BaseAsyncHandler
from logto import LogtoException
from services.auth_service import AuthService


class CallbackHandler(BaseAsyncHandler):
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    async def handle(
        self, request: Request, translator: Translator
    ) -> RedirectResponse:
        try:
            return await self._auth_service.handle_sign_in_callback(
                request, str(request.url)
            )
        except LogtoException as exc:
            detail = translator.gettext("error.sign_in_callback_failed").format(
                error=exc
            )
            raise HTTPException(status_code=400, detail=detail)
