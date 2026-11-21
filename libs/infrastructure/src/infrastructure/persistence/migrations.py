"""Programmatic Alembic entry points."""

from pathlib import Path
from typing import Final

from alembic import command
from alembic.config import Config

INFRASTRUCTURE_ROOT: Final[Path] = Path(__file__).resolve().parents[3]
ALEMBIC_INI_PATH: Final[Path] = INFRASTRUCTURE_ROOT / "alembic.ini"

DEFAULT_REVISION: Final[str] = "head"


def build_config() -> Config:
    """Build an Alembic config pointing at the infrastructure migrations."""
    return Config(str(ALEMBIC_INI_PATH))


def upgrade(revision: str = DEFAULT_REVISION) -> None:
    """Apply migrations up to the target revision."""
    command.upgrade(build_config(), revision)


def downgrade(revision: str) -> None:
    """Roll back migrations to the target revision."""
    command.downgrade(build_config(), revision)


def revision(message: str, *, autogenerate: bool = False) -> None:
    """Create a new migration revision."""
    command.revision(
        build_config(),
        message=message,
        autogenerate=autogenerate,
    )


def current() -> None:
    """Print the current database revision."""
    command.current(build_config())


def history() -> None:
    """Print the migration history."""
    command.history(build_config())


def check() -> None:
    """Fail when models and migrations are out of sync."""
    command.check(build_config())


def stamp(revision: str) -> None:
    """Set the database revision without running migrations."""
    command.stamp(build_config(), revision)
