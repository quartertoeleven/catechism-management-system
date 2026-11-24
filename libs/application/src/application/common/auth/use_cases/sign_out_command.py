"""Command ending the browser session."""

from cqrs import Request, Response

from application.common.auth.models import Session


class SignOutResult(Response):
    """URL the browser should be redirected to."""

    redirect_url: str


class SignOutCommand(Request[SignOutResult]):
    """Ask to end the current session."""

    session: Session | None = None
