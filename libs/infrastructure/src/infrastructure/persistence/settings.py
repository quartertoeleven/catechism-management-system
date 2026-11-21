"""Database configuration."""

from pathlib import Path
from typing import Final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

REPOSITORY_ROOT: Final[Path] = Path(__file__).resolve().parents[5]
ENV_FILE: Final[Path] = REPOSITORY_ROOT / ".env"
DATABASE_URL_ENV: Final[str] = "DATABASE_URL"


class DatabaseSettings(BaseSettings):
    """Settings required to connect to PostgreSQL."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(validation_alias=DATABASE_URL_ENV)
