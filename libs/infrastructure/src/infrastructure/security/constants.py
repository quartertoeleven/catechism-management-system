"""Constants for security infrastructure."""

from typing import Final

LOGTO_DISCOVERY_PATH: Final[str] = "/oidc/.well-known/openid-configuration"
HTTP_TIMEOUT_SECONDS: Final[float] = 10.0
JWKS_CACHE_TTL_SECONDS: Final[int] = 3600
PKCE_CODE_CHALLENGE_METHOD: Final[str] = "S256"
DEFAULT_LOGTO_SCOPES: Final[str] = "openid profile email offline_access"
DEFAULT_SESSION_COOKIE_NAME: Final[str] = "cms_session"
DEFAULT_SESSION_MAX_AGE_SECONDS: Final[int] = 14 * 24 * 3600
ENCRYPTION_KEY_SEPARATOR: Final[str] = ","
ID_TOKEN_LEEWAY_SECONDS: Final[int] = 0
