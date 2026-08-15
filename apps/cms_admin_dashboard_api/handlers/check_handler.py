from fastapi import HTTPException, Request
from logto import IdTokenClaims

from services.auth_service import AuthService


class CheckHandler:
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    def get_current_user(self, request: Request) -> IdTokenClaims:
        claims = self._auth_service.get_current_user(request)
        if claims is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return claims
