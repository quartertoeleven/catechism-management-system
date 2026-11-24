"""Handler for the start sign-in command."""

from cqrs import RequestHandler

from application.common.auth.redirects import safe_return_to
from application.common.auth.service import AuthenticationService
from application.common.auth.use_cases.start_sign_in_command import (
    StartSignInCommand,
    StartSignInResult,
)


class StartSignInHandler(RequestHandler[StartSignInCommand, StartSignInResult]):
    """Build the provider authorization URL and flow state."""

    def __init__(self, service: AuthenticationService) -> None:
        self._service = service

    async def handle(self, request: StartSignInCommand) -> StartSignInResult:
        """Start the sign-in flow."""
        url, flow = await self._service.start_sign_in(
            return_to=safe_return_to(request.return_to)
        )
        return StartSignInResult(authorization_url=url, flow=flow)
