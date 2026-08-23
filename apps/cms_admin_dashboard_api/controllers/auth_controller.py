from cms_locale import Translator
from containers import ApplicationContainer
from dependencies.locale_dependency import get_locale_translator
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from handlers.callback_handler import CallbackHandler
from handlers.check_handler import CheckHandler
from handlers.login_handler import LoginHandler
from handlers.logout_handler import LogoutHandler
from handlers.profile_handler import ProfileHandler
from models.check_response import CheckResponse
from models.user_profile import UserProfileResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login")
@inject
async def login(
    request: Request,
    login_handler: LoginHandler = Depends(Provide[ApplicationContainer.login_handler]),
) -> RedirectResponse:
    return await login_handler(request)


@router.get("/callback")
@inject
async def callback(
    request: Request,
    callback_handler: CallbackHandler = Depends(
        Provide[ApplicationContainer.callback_handler]
    ),
    translator: Translator = Depends(get_locale_translator),
) -> RedirectResponse:
    return await callback_handler(request, translator)


@router.get("/logout")
@inject
async def logout(
    request: Request,
    logout_handler: LogoutHandler = Depends(
        Provide[ApplicationContainer.logout_handler]
    ),
) -> RedirectResponse:
    return await logout_handler(request)


@router.get("/me")
@inject
async def my_profile(
    request: Request,
    profile_handler: ProfileHandler = Depends(
        Provide[ApplicationContainer.profile_handler]
    ),
) -> UserProfileResponse:
    return await profile_handler(request)


@router.get("/check")
@inject
async def check(
    request: Request,
    check_handler: CheckHandler = Depends(Provide[ApplicationContainer.check_handler]),
    translator: Translator = Depends(get_locale_translator),
) -> CheckResponse:
    return await check_handler(request, translator)
