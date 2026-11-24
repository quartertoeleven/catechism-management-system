"""Command starting the authorization code flow."""

from cqrs import Request, Response

from application.common.auth.models import FlowState


class StartSignInResult(Response):
    """Authorization URL and the flow state that must be persisted."""

    authorization_url: str
    flow: FlowState


class StartSignInCommand(Request[StartSignInResult]):
    """Ask to begin a sign-in flow for a return path."""

    return_to: str
