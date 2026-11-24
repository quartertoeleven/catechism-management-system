"""Command resolving the current session."""

from cqrs import Request, Response

from application.common.auth.models import Session
from application.common.auth.use_cases.views import CatechistView, UserView


class ResolveSessionResult(Response):
    """Authentication state derived from a session cookie."""

    authenticated: bool = False
    session: Session | None = None
    refreshed: bool = False
    expired: bool = False
    user: UserView | None = None
    catechist: CatechistView | None = None


class ResolveSessionCommand(Request[ResolveSessionResult]):
    """Ask to resolve a stored session, refreshing tokens if needed."""

    session: Session | None = None
