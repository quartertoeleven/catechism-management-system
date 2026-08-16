from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import Provide, inject
from fastapi.responses import RedirectResponse
from cms_locale import Translator

from containers import ApplicationContainer
from dependencies.locale_dependency import get_locale_translator
from handlers.login_handler import LoginHandler
from handlers.callback_handler import CallbackHandler
from handlers.logout_handler import LogoutHandler
from handlers.check_handler import CheckHandler
from services.auth_service import AuthService
from cms_common.profile import ProfileHandler, UserProfileResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
@inject
async def login(
    request: Request,
    login_handler: LoginHandler = Depends(Provide[ApplicationContainer.login_handler]),
) -> RedirectResponse:
    return await login_handler.build_sign_in_url(request)


@router.get("/callback")
@inject
async def callback(
    request: Request,
    callback_handler: CallbackHandler = Depends(
        Provide[ApplicationContainer.callback_handler]
    ),
    translator: Translator = Depends(get_locale_translator),
) -> RedirectResponse:
    return await callback_handler.handle_sign_in_callback(request, translator)


@router.get("/logout")
@inject
async def logout(
    request: Request,
    logout_handler: LogoutHandler = Depends(Provide[ApplicationContainer.logout_handler]),
) -> RedirectResponse:
    return await logout_handler.build_sign_out_url(request)


@router.get("/me")
@inject
async def my_profile(
    request: Request,
    auth_service: AuthService = Depends(Provide[ApplicationContainer.auth_service]),
    profile_handler: ProfileHandler = Depends(
        Provide[ApplicationContainer.profile_handler]
    ),
) -> UserProfileResponse:
    client = auth_service.create_client(request)
    return await profile_handler.my_profile(client)


@router.get("/check")
@inject
async def check(
    request: Request,
    check_handler: CheckHandler = Depends(Provide[ApplicationContainer.check_handler]),
    translator: Translator = Depends(get_locale_translator),
) -> dict:
    claims = check_handler.get_current_user(request, translator)
    return {"authenticated": True, "sub": claims.sub}
