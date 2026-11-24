"""Authentication orchestration."""

from __future__ import annotations

import secrets
import uuid
from dataclasses import replace

from domain.directory import Catechist, CatechistRepository

from application.common.auth.constants import (
    NONCE_BYTE_LENGTH,
    PKCE_VERIFIER_BYTE_LENGTH,
    STATE_BYTE_LENGTH,
)
from application.common.auth.errors import AuthenticationError, CatechistLinkError
from application.common.auth.models import FlowState, Session
from application.common.auth.ports import IdentityProvider


class AuthenticationService:
    """Coordinate the authorization code flow with an identity provider."""

    def __init__(
        self,
        provider: IdentityProvider,
        catechists: CatechistRepository,
    ) -> None:
        self._provider = provider
        self._catechists = catechists

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

    async def complete_sign_in(
        self, *, code: str, flow: FlowState, state: str
    ) -> Session:
        """Exchange the authorization code and build a session."""
        if not secrets.compare_digest(flow.state, state):
            raise AuthenticationError("Authorization state mismatch")
        exchange = await self._provider.exchange_code(
            code=code,
            code_verifier=flow.code_verifier,
            nonce=flow.nonce,
        )
        profile = await self._provider.userinfo(
            access_token=exchange.tokens.access_token
        )
        catechist = await self._resolve_catechist(exchange.catechist_id)
        return Session(
            profile=profile,
            tokens=exchange.tokens,
            catechist_id=catechist.id,
        )

    async def _resolve_catechist(self, catechist_id: str | None) -> Catechist:
        """Return the linked catechist or fail the sign-in attempt."""
        if not catechist_id:
            raise CatechistLinkError("Catechist link missing")

        try:
            parsed_id = uuid.UUID(catechist_id)
        except ValueError:
            raise CatechistLinkError("Catechist link invalid") from None

        catechist = await self._catechists.get(parsed_id)
        if catechist is None:
            raise CatechistLinkError("Catechist link unresolved")
        return catechist

    async def refresh_session(self, session: Session) -> Session | None:
        """Return a usable session, refreshing tokens when needed."""
        if not session.tokens.needs_refresh():
            return session

        refresh_token = session.tokens.refresh_token
        if refresh_token is None:
            return None if session.tokens.is_expired() else session

        try:
            tokens = await self._provider.refresh(refresh_token=refresh_token)
        except AuthenticationError:
            return None if session.tokens.is_expired() else session

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
