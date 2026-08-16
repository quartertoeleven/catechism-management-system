from pathlib import Path

from pydantic import BaseModel, Field

DEFAULT_LOCALE = "en"
DEFAULT_SUPPORTED_LOCALES = ("en", "vi")


class LocaleConfig(BaseModel):
    catalogs_dir: Path
    default_locale: str = Field(default=DEFAULT_LOCALE)
    supported_locales: tuple[str, ...] = Field(default=DEFAULT_SUPPORTED_LOCALES)
    fallback_locale: str | None = Field(default=DEFAULT_LOCALE)
