"""Async engine and session factory construction."""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from infrastructure.persistence.settings import DatabaseSettings

SESSION_EXPIRE_ON_COMMIT: bool = False


def build_engine(settings: DatabaseSettings) -> AsyncEngine:
    """Create an async engine for the configured database."""
    return create_async_engine(settings.database_url)


def build_session_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Create a session factory bound to the given engine."""
    return async_sessionmaker(engine, expire_on_commit=SESSION_EXPIRE_ON_COMMIT)
