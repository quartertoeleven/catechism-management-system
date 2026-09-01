from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request
from logto import IdTokenClaims
from services.auth_service import AuthService


@inject
async def get_authenticated_user(
    request: Request,
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
) -> IdTokenClaims:
    claims = await auth_service.get_current_user(request)
    if claims is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return claims
