"""Encrypted cookie storage for session and flow state."""

from __future__ import annotations

import json
import uuid
import zlib
from datetime import UTC, datetime
from typing import Any, Final, cast

from application.common.auth.models import (
    FlowState,
    Session,
    TokenSet,
    UserProfile,
)
from cryptography.fernet import InvalidToken, MultiFernet

COMPRESSED_MARKER: Final[bytes] = b"z1:"
COMPRESSION_LEVEL: Final[int] = 9


class EncryptedCookieSessionStore:
    """Encode and decode session payloads with Fernet."""

    def __init__(self, fernet: MultiFernet) -> None:
        self._fernet = fernet

    def read(self, raw: str | None) -> Session | None:
        """Decode a raw session cookie."""
        payload = _decrypt(self._fernet, raw)
        if payload is None:
            return None
        try:
            return _session_from_payload(payload)
        except KeyError, TypeError, ValueError:
            return None

    def write(self, session: Session) -> str:
        """Encode a session into a raw cookie value."""
        payload = _session_to_payload(session)
        return _encrypt(self._fernet, payload)


class EncryptedCookieFlowStore:
    """Encode and decode authorization flow payloads with Fernet."""

    def __init__(self, fernet: MultiFernet) -> None:
        self._fernet = fernet

    def read(self, raw: str | None) -> FlowState | None:
        """Decode a raw flow cookie."""
        payload = _decrypt(self._fernet, raw)
        if payload is None:
            return None
        try:
            return FlowState(
                state=str(payload["state"]),
                nonce=str(payload["nonce"]),
                code_verifier=str(payload["code_verifier"]),
                return_to=str(payload["return_to"]),
            )
        except KeyError:
            return None

    def write(self, flow: FlowState) -> str:
        """Encode flow state into a raw cookie value."""
        return _encrypt(
            self._fernet,
            {
                "state": flow.state,
                "nonce": flow.nonce,
                "code_verifier": flow.code_verifier,
                "return_to": flow.return_to,
            },
        )


def _encrypt(fernet: MultiFernet, payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, separators=(",", ":")).encode()
    compressed = zlib.compress(serialized, COMPRESSION_LEVEL)
    return fernet.encrypt(COMPRESSED_MARKER + compressed).decode()


def _decrypt(fernet: MultiFernet, raw: str | None) -> dict[str, Any] | None:
    if not raw:
        return None
    try:
        data = fernet.decrypt(raw.encode())
        if data.startswith(COMPRESSED_MARKER):
            data = zlib.decompress(data[len(COMPRESSED_MARKER) :])
        payload = json.loads(data.decode())
    except InvalidToken, ValueError, zlib.error:
        return None
    if not isinstance(payload, dict):
        return None
    return cast(dict[str, Any], payload)


def _session_to_payload(session: Session) -> dict[str, Any]:
    return {
        "profile": {
            "subject": session.profile.subject,
            "name": session.profile.name,
            "email": session.profile.email,
            "picture": session.profile.picture,
        },
        "tokens": {
            "access_token": session.tokens.access_token,
            "refresh_token": session.tokens.refresh_token,
            "id_token": session.tokens.id_token,
            "expires_at": session.tokens.expires_at.isoformat(),
        },
        "catechist_id": (str(session.catechist_id) if session.catechist_id else None),
    }


def _session_from_payload(payload: dict[str, Any]) -> Session:
    profile_payload = cast(dict[str, Any], payload["profile"])
    tokens_payload = cast(dict[str, Any], payload["tokens"])

    expires_at = datetime.fromisoformat(str(tokens_payload["expires_at"]))
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)

    catechist_raw = payload.get("catechist_id")

    return Session(
        profile=UserProfile(
            subject=str(profile_payload["subject"]),
            name=_optional_string(profile_payload.get("name")),
            email=_optional_string(profile_payload.get("email")),
            picture=_optional_string(profile_payload.get("picture")),
        ),
        tokens=TokenSet(
            access_token=str(tokens_payload["access_token"]),
            refresh_token=_optional_string(tokens_payload.get("refresh_token")),
            id_token=_optional_string(tokens_payload.get("id_token")),
            expires_at=expires_at,
        ),
        catechist_id=(uuid.UUID(str(catechist_raw)) if catechist_raw else None),
    )


def _optional_string(value: object) -> str | None:
    return None if value is None else str(value)
