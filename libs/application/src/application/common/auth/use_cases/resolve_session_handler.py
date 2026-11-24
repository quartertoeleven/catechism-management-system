"""Handler for the resolve session command."""

from cqrs import RequestHandler
from domain.directory.repositories import CatechistRepository

from application.common.auth.models import Session
from application.common.auth.service import AuthenticationService
from application.common.auth.use_cases.resolve_session_command import (
    ResolveSessionCommand,
    ResolveSessionResult,
)
from application.common.auth.use_cases.views import CatechistView, UserView


class ResolveSessionHandler(
    RequestHandler[ResolveSessionCommand, ResolveSessionResult]
):
    """Refresh the session when required and describe the authenticated user."""

    def __init__(
        self,
        service: AuthenticationService,
        catechists: CatechistRepository,
    ) -> None:
        self._service = service
        self._catechists = catechists

    async def handle(
        self,
        request: ResolveSessionCommand,
    ) -> ResolveSessionResult:
        """Resolve the stored session into a view."""
        if request.session is None:
            return ResolveSessionResult()

        refreshed = await self._service.refresh_session(request.session)
        if refreshed is None:
            return ResolveSessionResult(expired=True)

        return ResolveSessionResult(
            authenticated=True,
            session=refreshed,
            refreshed=refreshed is not request.session,
            user=_user_view(refreshed),
            catechist=await self._catechist_view(refreshed),
        )

    async def _catechist_view(self, session: Session) -> CatechistView | None:
        if session.catechist_id is None:
            return None

        catechist = await self._catechists.get(session.catechist_id)
        if catechist is None:
            return None

        return CatechistView(
            id=catechist.id,
            code=catechist.code,
            full_name=catechist.full_name,
        )


def _user_view(session: Session) -> UserView:
    return UserView(
        subject=session.profile.subject,
        name=session.profile.name,
        email=session.profile.email,
        picture=session.profile.picture,
    )
