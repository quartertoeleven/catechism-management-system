"""Session cookie helpers shared by controllers and dependencies."""

from typing import Final

from fastapi import Response
from infrastructure.security.constants import COOKIE_PATH, COOKIE_SAMESITE
from infrastructure.security.logto.settings import LogtoSettings

SET_COOKIE_HEADER: Final[str] = "set-cookie"


def set_session_cookie(
    response: Response,
    settings: LogtoSettings,
    raw: str,
) -> None:
    """Attach the encrypted session cookie to a response."""
    response.set_cookie(
        settings.session_cookie_name,
        raw,
        max_age=settings.session_max_age_seconds,
        path=COOKIE_PATH,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite=COOKIE_SAMESITE,
    )


def clear_session_cookie(response: Response, settings: LogtoSettings) -> None:
    """Remove the session cookie from a response."""
    response.delete_cookie(settings.session_cookie_name, path=COOKIE_PATH)


def clear_session_cookie_header(settings: LogtoSettings) -> dict[str, str]:
    """Build a Set-Cookie header that removes the session cookie."""
    response = Response()
    clear_session_cookie(response, settings)
    return {SET_COOKIE_HEADER: response.headers[SET_COOKIE_HEADER]}
