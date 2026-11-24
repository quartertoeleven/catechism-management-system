"""Handler for the sign-out command."""

from cqrs import RequestHandler

from application.common.auth.constants import DEFAULT_RETURN_TO
from application.common.auth.errors import AuthenticationError
from application.common.auth.service import AuthenticationService
from application.common.auth.use_cases.sign_out_command import (
    SignOutCommand,
    SignOutResult,
)


class SignOutHandler(RequestHandler[SignOutCommand, SignOutResult]):
    """Build the provider sign-out URL."""

    def __init__(self, service: AuthenticationService) -> None:
        self._service = service

    async def handle(self, request: SignOutCommand) -> SignOutResult:
        """Return the URL to redirect to after ending the session."""
        try:
            url = await self._service.sign_out(request.session)
        except AuthenticationError:
            url = DEFAULT_RETURN_TO
        return SignOutResult(redirect_url=url)
