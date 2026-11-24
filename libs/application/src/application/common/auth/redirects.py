"""Validation helpers for post-authentication redirects."""

from __future__ import annotations

from typing import Final

from application.common.auth.constants import DEFAULT_RETURN_TO

LOCAL_PATH_PREFIX: Final[str] = "/"
PROTOCOL_RELATIVE_PREFIX: Final[str] = "//"
BACKSLASH: Final[str] = "\\"


def safe_return_to(candidate: str | None) -> str:
    """Return a local path for redirects, falling back to the default."""
    if not candidate:
        return DEFAULT_RETURN_TO
    if not candidate.startswith(LOCAL_PATH_PREFIX):
        return DEFAULT_RETURN_TO
    if candidate.startswith(PROTOCOL_RELATIVE_PREFIX):
        return DEFAULT_RETURN_TO
    if BACKSLASH in candidate or _has_control_characters(candidate):
        return DEFAULT_RETURN_TO
    return candidate


def _has_control_characters(value: str) -> bool:
    return any(character < " " or character == "\x7f" for character in value)
