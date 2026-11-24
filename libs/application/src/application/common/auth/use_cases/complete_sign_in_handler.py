"""Handler for the complete sign-in command."""

from cqrs import RequestHandler

from application.common.auth.redirects import safe_return_to
from application.common.auth.service import AuthenticationService
from application.common.auth.use_cases.complete_sign_in_command import (
    CompleteSignInCommand,
    CompleteSignInResult,
)


class CompleteSignInHandler(
    RequestHandler[CompleteSignInCommand, CompleteSignInResult]
):
    """Exchange the authorization code and build a session."""

    def __init__(self, service: AuthenticationService) -> None:
        self._service = service

    async def handle(
        self,
        request: CompleteSignInCommand,
    ) -> CompleteSignInResult:
        """Complete the sign-in flow."""
        session = await self._service.complete_sign_in(
            code=request.code,
            flow=request.flow,
            state=request.state,
        )
        return CompleteSignInResult(
            session=session,
            return_to=safe_return_to(request.flow.return_to),
        )
