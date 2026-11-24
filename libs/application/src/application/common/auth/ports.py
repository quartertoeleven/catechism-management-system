"""Ports implemented by authentication infrastructure."""

from __future__ import annotations

from typing import Protocol

from application.common.auth.models import (
    CodeExchangeResult,
    FlowState,
    Session,
    TokenSet,
    UserProfile,
)


class IdentityProvider(Protocol):
    """OIDC identity provider operations."""

    async def authorization_url(
        self, *, state: str, nonce: str, code_verifier: str
    ) -> str:
        """Build the authorization URL for the given flow values."""
        ...

    async def exchange_code(
        self, *, code: str, code_verifier: str, nonce: str
    ) -> CodeExchangeResult:
        """Exchange an authorization code for tokens and identity claims."""
        ...

    async def refresh(self, *, refresh_token: str) -> TokenSet:
        """Exchange a refresh token for a new token set."""
        ...

    async def userinfo(self, *, access_token: str) -> UserProfile:
        """Fetch profile claims from the userinfo endpoint."""
        ...

    async def end_session_url(self, *, id_token: str | None) -> str:
        """Build the provider logout URL."""
        ...


class SessionStore(Protocol):
    """Encode and decode session cookies."""

    def read(self, raw: str | None) -> Session | None:
        """Decode a raw cookie value."""
        ...

    def write(self, session: Session) -> str:
        """Encode a session into a raw cookie value."""
        ...


class FlowStore(Protocol):
    """Encode and decode authorization flow cookies."""

    def read(self, raw: str | None) -> FlowState | None:
        """Decode a raw flow cookie value."""
        ...

    def write(self, flow: FlowState) -> str:
        """Encode a flow state into a raw cookie value."""
        ...
