"""Logto configuration."""

from typing import Final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from infrastructure.persistence.settings import ENV_FILE
from infrastructure.security.constants import (
    DEFAULT_LOGTO_SCOPES,
    DEFAULT_SESSION_COOKIE_NAME,
    DEFAULT_SESSION_MAX_AGE_SECONDS,
    LOGTO_DISCOVERY_PATH,
)

LOGTO_ENDPOINT_ENV: Final[str] = "LOGTO_ENDPOINT"
LOGTO_APP_ID_ENV: Final[str] = "LOGTO_APP_ID"
LOGTO_APP_SECRET_ENV: Final[str] = "LOGTO_APP_SECRET"
LOGTO_REDIRECT_URI_ENV: Final[str] = "LOGTO_REDIRECT_URI"
LOGTO_POST_LOGOUT_REDIRECT_URI_ENV: Final[str] = "LOGTO_POST_LOGOUT_REDIRECT_URI"
LOGTO_SCOPES_ENV: Final[str] = "LOGTO_SCOPES"
SESSION_ENCRYPTION_KEY_ENV: Final[str] = "SESSION_ENCRYPTION_KEY"
SESSION_COOKIE_NAME_ENV: Final[str] = "SESSION_COOKIE_NAME"
SESSION_COOKIE_SECURE_ENV: Final[str] = "SESSION_COOKIE_SECURE"
SESSION_MAX_AGE_SECONDS_ENV: Final[str] = "SESSION_MAX_AGE_SECONDS"


class LogtoSettings(BaseSettings):
    """Settings required to talk to Logto."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    endpoint: str = Field(validation_alias=LOGTO_ENDPOINT_ENV)
    app_id: str = Field(validation_alias=LOGTO_APP_ID_ENV)
    app_secret: str = Field(validation_alias=LOGTO_APP_SECRET_ENV)
    redirect_uri: str = Field(validation_alias=LOGTO_REDIRECT_URI_ENV)
    post_logout_redirect_uri: str = Field(
        validation_alias=LOGTO_POST_LOGOUT_REDIRECT_URI_ENV
    )
    scopes: str = Field(
        default=DEFAULT_LOGTO_SCOPES,
        validation_alias=LOGTO_SCOPES_ENV,
    )
    session_encryption_key: str = Field(validation_alias=SESSION_ENCRYPTION_KEY_ENV)
    session_cookie_name: str = Field(
        default=DEFAULT_SESSION_COOKIE_NAME,
        validation_alias=SESSION_COOKIE_NAME_ENV,
    )
    session_cookie_secure: bool = Field(
        default=False,
        validation_alias=SESSION_COOKIE_SECURE_ENV,
    )
    session_max_age_seconds: int = Field(
        default=DEFAULT_SESSION_MAX_AGE_SECONDS,
        validation_alias=SESSION_MAX_AGE_SECONDS_ENV,
    )

    @property
    def discovery_url(self) -> str:
        """Return the OIDC discovery URL."""
        return f"{self.endpoint.rstrip('/')}{LOGTO_DISCOVERY_PATH}"

    @property
    def scope_list(self) -> list[str]:
        """Return configured scopes as a list."""
        return self.scopes.split()
