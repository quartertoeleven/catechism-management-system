"""Command completing the authorization code flow."""

from cqrs import Request, Response

from application.common.auth.models import FlowState, Session


class CompleteSignInResult(Response):
    """Authenticated session and the path to return to."""

    session: Session
    return_to: str


class CompleteSignInCommand(Request[CompleteSignInResult]):
    """Ask to finish a sign-in flow with the provider callback values."""

    code: str
    flow: FlowState
    state: str
