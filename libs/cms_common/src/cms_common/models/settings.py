from typing import Annotated

from pydantic import BeforeValidator, Field
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


def _split_comma(value: str | list[str]) -> list[str]:
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return value


CommaSeparatedList = Annotated[list[str], NoDecode, BeforeValidator(_split_comma)]


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict()

    session_secret: str = Field(default="", validation_alias="AUTH_SESSION_SECRET")
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/catechism_management_system",
        validation_alias="DATABASE_URL",
    )
    cookie_name: str = Field(default="cms_session", validation_alias="AUTH_SESSION_NAME")
    cookie_secure: bool = Field(default=False, validation_alias="AUTH_SESSION_SECURE")
    cookie_samesite: str = Field(default="lax", validation_alias="AUTH_SESSION_SAMESITE")
    cookie_max_age: int = Field(default=2592000, validation_alias="AUTH_SESSION_MAX_AGE")


class CmsAdminDashboardSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CMS_ADMIN_DASHBOARD_")

    common: CommonSettings = CommonSettings()

    version: str = "0.1.0"
    frontend_url: str = "http://localhost:3000"
    cors_origins: CommaSeparatedList = ["http://localhost:3000"]
    logto_endpoint: str = ""
    logto_app_id: str = ""
    logto_app_secret: str = ""
    logto_redirect_uri: str = "http://localhost:8000/dashboard-api/auth/callback"
    logto_resources: CommaSeparatedList = []
    locale_catalogs_dir: str = "apps/cms_admin_dashboard_api/translations"
    locale_default_locale: str = "vi"
    locale_supported_locales: CommaSeparatedList = ["en", "vi"]
    locale_fallback_locale: str = "vi"
