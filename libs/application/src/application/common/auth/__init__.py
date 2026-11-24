"""Authentication application services."""

from application.common.auth.constants import DEFAULT_RETURN_TO
from application.common.auth.errors import AuthenticationError, CatechistLinkError
from application.common.auth.models import (
    CodeExchangeResult,
    FlowState,
    Session,
    TokenSet,
    UserProfile,
)
from application.common.auth.ports import (
    FlowStore,
    IdentityProvider,
    SessionStore,
)
from application.common.auth.redirects import safe_return_to
from application.common.auth.service import AuthenticationService

__all__ = (
    "DEFAULT_RETURN_TO",
    "AuthenticationError",
    "AuthenticationService",
    "CatechistLinkError",
    "CodeExchangeResult",
    "FlowState",
    "FlowStore",
    "IdentityProvider",
    "Session",
    "SessionStore",
    "TokenSet",
    "UserProfile",
    "safe_return_to",
)
