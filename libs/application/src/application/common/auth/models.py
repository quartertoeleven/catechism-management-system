"""Authentication models."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from application.common.auth.constants import ACCESS_TOKEN_LEEWAY_SECONDS


@dataclass(frozen=True, slots=True)
class TokenSet:
    """Tokens issued by the identity provider."""

    access_token: str
    refresh_token: str | None
    id_token: str | None
    expires_at: datetime

    def is_expired(self) -> bool:
        """Return whether the access token is expired or about to expire."""
        threshold = datetime.now(tz=UTC) + timedelta(
            seconds=ACCESS_TOKEN_LEEWAY_SECONDS
        )
        return self.expires_at <= threshold


@dataclass(frozen=True, slots=True)
class UserProfile:
    """Profile claims of the authenticated user."""

    subject: str
    name: str | None = None
    email: str | None = None
    picture: str | None = None


@dataclass(frozen=True, slots=True)
class Session:
    """Authenticated browser session."""

    profile: UserProfile
    tokens: TokenSet
    catechist_id: uuid.UUID | None = None


@dataclass(frozen=True, slots=True)
class FlowState:
    """Transient state kept during the authorization code flow."""

    state: str
    nonce: str
    code_verifier: str
    return_to: str
