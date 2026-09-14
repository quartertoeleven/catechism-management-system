from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Request, Response
from logto import IdTokenClaims
from services.auth_service import AuthService


@inject
async def get_authenticated_user(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
) -> IdTokenClaims:
    claims = await auth_service.get_current_user(request, response)
    if claims is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return claims
