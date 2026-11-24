"""FastAPI dependencies shared by protected controllers."""

from typing import Final

from application.common.auth import Session, SessionStore
from application.common.auth.use_cases.resolve_session_command import (
    ResolveSessionCommand,
)
from cqrs import RequestMediator
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import HTTPException, Request, Response, status
from infrastructure.security.logto.settings import LogtoSettings

from admin_dashboard_api.cookies import (
    clear_session_cookie_header,
    set_session_cookie,
)

UNAUTHENTICATED_DETAIL: Final[str] = "Authentication required"


@inject
async def require_session(
    request: Request,
    response: Response,
    settings: FromDishka[LogtoSettings],
    sessions: FromDishka[SessionStore],
    mediator: FromDishka[RequestMediator],
) -> Session:
    """Refresh the session when near expiry, or fail with HTTP 401."""
    session = sessions.read(request.cookies.get(settings.session_cookie_name))
    result = await mediator.send(ResolveSessionCommand(session=session))

    if not result.authenticated or result.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UNAUTHENTICATED_DETAIL,
            headers=clear_session_cookie_header(settings),
        )

    if result.refreshed:
        set_session_cookie(
            response,
            settings,
            sessions.write(result.session),
        )

    return result.session
