"""Authentication controller implementing the BFF sign-in flow."""

import uuid
from typing import Annotated, Final
from urllib.parse import urlencode

from application.common.auth import (
    DEFAULT_RETURN_TO,
    AuthenticationError,
    CatechistLinkError,
    FlowStore,
    SessionStore,
)
from application.common.auth.use_cases.complete_sign_in_command import (
    CompleteSignInCommand,
)
from application.common.auth.use_cases.resolve_session_command import (
    ResolveSessionCommand,
    ResolveSessionResult,
)
from application.common.auth.use_cases.sign_out_command import SignOutCommand
from application.common.auth.use_cases.start_sign_in_command import (
    StartSignInCommand,
)
from cqrs import RequestMediator
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse, Response
from infrastructure.security.constants import (
    COOKIE_PATH,
    COOKIE_SAMESITE,
    FLOW_COOKIE_MAX_AGE_SECONDS,
)
from infrastructure.security.logto.settings import LogtoSettings
from pydantic import BaseModel

from admin_dashboard_api.cookies import set_session_cookie

router = APIRouter(prefix="/auth", tags=["auth"])

LOGIN_PATH: Final[str] = "/login"
ERROR_QUERY: Final[str] = "error"
INVALID_FLOW_ERROR: Final[str] = "invalid_flow"
MISSING_CODE_ERROR: Final[str] = "missing_code"
AUTHENTICATION_FAILED_ERROR: Final[str] = "authentication_failed"
CATECHIST_NOT_LINKED_ERROR: Final[str] = "catechist_not_linked"
REDIRECT_STATUS_CODE: Final[int] = 302


class CatechistResponse(BaseModel):
    """Catechist linked to the authenticated user."""

    id: uuid.UUID
    code: str
    full_name: str


class SessionUserResponse(BaseModel):
    """Profile claims exposed to the browser."""

    subject: str
    name: str | None = None
    email: str | None = None
    picture: str | None = None


class SessionResponse(BaseModel):
    """Current authentication state."""

    authenticated: bool
    user: SessionUserResponse | None = None
    catechist: CatechistResponse | None = None


@router.get("/login", response_class=RedirectResponse)
@inject
async def login(
    settings: FromDishka[LogtoSettings],
    flows: FromDishka[FlowStore],
    mediator: FromDishka[RequestMediator],
    return_to: Annotated[str, Query()] = DEFAULT_RETURN_TO,
) -> RedirectResponse:
    """Start the authorization code flow."""
    try:
        result = await mediator.send(StartSignInCommand(return_to=return_to))
    except AuthenticationError:
        return _error_redirect(settings, AUTHENTICATION_FAILED_ERROR)
    response = RedirectResponse(
        result.authorization_url,
        status_code=REDIRECT_STATUS_CODE,
    )
    response.set_cookie(
        settings.flow_cookie_name,
        flows.write(result.flow),
        max_age=FLOW_COOKIE_MAX_AGE_SECONDS,
        path=COOKIE_PATH,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite=COOKIE_SAMESITE,
    )
    return response


@router.get("/callback", response_class=RedirectResponse)
@inject
async def callback(
    request: Request,
    settings: FromDishka[LogtoSettings],
    flows: FromDishka[FlowStore],
    sessions: FromDishka[SessionStore],
    mediator: FromDishka[RequestMediator],
    code: Annotated[str | None, Query()] = None,
    state: Annotated[str | None, Query()] = None,
) -> RedirectResponse:
    """Complete the authorization code flow."""
    flow = flows.read(request.cookies.get(settings.flow_cookie_name))
    if flow is None or state is None:
        return _error_redirect(settings, INVALID_FLOW_ERROR)
    if code is None:
        return _error_redirect(settings, MISSING_CODE_ERROR)

    try:
        result = await mediator.send(
            CompleteSignInCommand(code=code, flow=flow, state=state)
        )
    except CatechistLinkError:
        return _error_redirect(settings, CATECHIST_NOT_LINKED_ERROR)
    except AuthenticationError:
        return _error_redirect(settings, AUTHENTICATION_FAILED_ERROR)

    response = RedirectResponse(
        result.return_to,
        status_code=REDIRECT_STATUS_CODE,
    )
    set_session_cookie(response, settings, sessions.write(result.session))
    response.delete_cookie(settings.flow_cookie_name, path=COOKIE_PATH)
    return response


@router.get("/session", response_model=SessionResponse)
@inject
async def current_session(
    request: Request,
    settings: FromDishka[LogtoSettings],
    sessions: FromDishka[SessionStore],
    mediator: FromDishka[RequestMediator],
) -> Response:
    """Return the browser's authentication state, refreshing tokens if needed."""
    session = sessions.read(request.cookies.get(settings.session_cookie_name))
    result = await mediator.send(ResolveSessionCommand(session=session))

    if not result.authenticated:
        response = _session_response(SessionResponse(authenticated=False))
        if result.expired:
            response.delete_cookie(settings.session_cookie_name, path=COOKIE_PATH)
        return response

    response = _session_response(_session_payload(result))
    if result.refreshed and result.session is not None:
        set_session_cookie(response, settings, sessions.write(result.session))
    return response


@router.get("/logout", response_class=RedirectResponse)
@inject
async def logout(
    request: Request,
    settings: FromDishka[LogtoSettings],
    sessions: FromDishka[SessionStore],
    mediator: FromDishka[RequestMediator],
) -> RedirectResponse:
    """Clear the session and redirect to the provider logout endpoint."""
    session = sessions.read(request.cookies.get(settings.session_cookie_name))
    result = await mediator.send(SignOutCommand(session=session))
    response = RedirectResponse(
        result.redirect_url,
        status_code=REDIRECT_STATUS_CODE,
    )
    response.delete_cookie(settings.session_cookie_name, path=COOKIE_PATH)
    response.delete_cookie(settings.flow_cookie_name, path=COOKIE_PATH)
    return response


def _session_payload(result: ResolveSessionResult) -> SessionResponse:
    return SessionResponse(
        authenticated=True,
        user=_session_user(result),
        catechist=_session_catechist(result),
    )


def _session_user(result: ResolveSessionResult) -> SessionUserResponse | None:
    if result.user is None:
        return None
    return SessionUserResponse(
        subject=result.user.subject,
        name=result.user.name,
        email=result.user.email,
        picture=result.user.picture,
    )


def _session_catechist(result: ResolveSessionResult) -> CatechistResponse | None:
    if result.catechist is None:
        return None
    return CatechistResponse(
        id=result.catechist.id,
        code=result.catechist.code,
        full_name=result.catechist.full_name,
    )


def _session_response(payload: SessionResponse) -> Response:
    return JSONResponse(content=payload.model_dump(mode="json"))


def _error_redirect(settings: LogtoSettings, error: str) -> RedirectResponse:
    query = urlencode({ERROR_QUERY: error})
    response = RedirectResponse(
        f"{LOGIN_PATH}?{query}",
        status_code=REDIRECT_STATUS_CODE,
    )
    response.delete_cookie(settings.flow_cookie_name, path=COOKIE_PATH)
    return response
