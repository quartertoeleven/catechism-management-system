from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject
from fastapi.responses import RedirectResponse
from logto import IdTokenClaims, LogtoException

from containers import ApplicationContainer
from dependencies.auth import get_current_user
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
@inject
async def login(
    request: Request,
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
) -> RedirectResponse:
    return await auth_service.build_sign_in_url(request)


@router.get("/callback")
@inject
async def callback(
    request: Request,
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
) -> RedirectResponse:
    try:
        return await auth_service.handle_sign_in_callback(request, str(request.url))
    except LogtoException as exc:
        raise HTTPException(status_code=400, detail=f"Sign-in callback failed: {exc}")


@router.get("/logout")
@inject
async def logout(
    request: Request,
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
) -> RedirectResponse:
    return await auth_service.build_sign_out_url(request)


@router.get("/me")
async def me(
    claims: IdTokenClaims = Depends(get_current_user),
) -> dict:
    return claims.model_dump(exclude_none=True)


@router.get("/check")
async def check(
    claims: IdTokenClaims = Depends(get_current_user),
) -> dict:
    return {"authenticated": True, "sub": claims.sub}
