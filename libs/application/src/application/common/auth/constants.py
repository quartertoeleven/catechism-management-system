"""Constants for authentication flows."""

from typing import Final

DEFAULT_RETURN_TO: Final[str] = "/"
PKCE_VERIFIER_BYTE_LENGTH: Final[int] = 64
STATE_BYTE_LENGTH: Final[int] = 32
NONCE_BYTE_LENGTH: Final[int] = 32
ACCESS_TOKEN_REFRESH_WINDOW_SECONDS: Final[int] = 5 * 60
