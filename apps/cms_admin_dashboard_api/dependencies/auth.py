from fastapi import Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject
from logto import IdTokenClaims

from containers import ApplicationContainer
from services.auth_service import AuthService


@inject
async def get_current_user(
    request: Request,
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
) -> IdTokenClaims:
    claims = auth_service.get_current_user(request)
    if claims is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return claims
