"""Authentication orchestration."""

from __future__ import annotations

import secrets
from dataclasses import replace

from application.common.auth.constants import (
    NONCE_BYTE_LENGTH,
    PKCE_VERIFIER_BYTE_LENGTH,
    STATE_BYTE_LENGTH,
)
from application.common.auth.errors import AuthenticationError
from application.common.auth.models import FlowState, Session
from application.common.auth.ports import IdentityProvider


class AuthenticationService:
    """Coordinate the authorization code flow with an identity provider."""

    def __init__(self, provider: IdentityProvider) -> None:
        self._provider = provider

    async def start_sign_in(self, *, return_to: str) -> tuple[str, FlowState]:
        """Create flow state and return the authorization URL."""
        flow = FlowState(
            state=secrets.token_urlsafe(STATE_BYTE_LENGTH),
            nonce=secrets.token_urlsafe(NONCE_BYTE_LENGTH),
            code_verifier=secrets.token_urlsafe(PKCE_VERIFIER_BYTE_LENGTH),
            return_to=return_to,
        )
        url = await self._provider.authorization_url(
            state=flow.state,
            nonce=flow.nonce,
            code_verifier=flow.code_verifier,
        )
        return url, flow

    async def complete_sign_in(self, *, code: str, flow: FlowState) -> Session:
        """Exchange the authorization code and build a session."""
        tokens = await self._provider.exchange_code(
            code=code,
            code_verifier=flow.code_verifier,
            nonce=flow.nonce,
        )
        profile = await self._provider.userinfo(access_token=tokens.access_token)
        return Session(profile=profile, tokens=tokens)

    async def refresh_session(self, session: Session) -> Session | None:
        """Return a usable session, refreshing tokens when needed."""
        if not session.tokens.is_expired():
            return session

        refresh_token = session.tokens.refresh_token
        if refresh_token is None:
            return None

        try:
            tokens = await self._provider.refresh(refresh_token=refresh_token)
        except AuthenticationError:
            return None

        if tokens.refresh_token is None:
            tokens = replace(tokens, refresh_token=refresh_token)

        return Session(
            profile=session.profile,
            tokens=tokens,
            catechist_id=session.catechist_id,
        )

    async def sign_out(self, session: Session | None) -> str:
        """Return the provider logout URL."""
        id_token = session.tokens.id_token if session else None
        return await self._provider.end_session_url(id_token=id_token)
