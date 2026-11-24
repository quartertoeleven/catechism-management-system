"""Persistence dependency injection provider."""

from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from domain.directory.repositories import CatechistRepository
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from infrastructure.persistence.directory.repository import (
    SqlAlchemyCatechistRepository,
)
from infrastructure.persistence.engine import build_engine, build_session_factory
from infrastructure.persistence.settings import DatabaseSettings


class PersistenceProvider(Provider):
    """Provide database engines, sessions and repositories."""

    @provide(scope=Scope.APP)
    def settings(self) -> DatabaseSettings:
        """Build database settings from the environment."""
        return DatabaseSettings()

    @provide(scope=Scope.APP)
    async def engine(
        self,
        settings: DatabaseSettings,
    ) -> AsyncIterator[AsyncEngine]:
        """Provide the shared database engine."""
        engine = build_engine(settings)
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.APP)
    def session_factory(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        """Provide the session factory bound to the shared engine."""
        return build_session_factory(engine)

    @provide(scope=Scope.REQUEST)
    async def session(
        self,
        factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        """Provide a request-scoped database session."""
        async with factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @provide(scope=Scope.REQUEST)
    def catechist_repository(
        self,
        session: AsyncSession,
    ) -> CatechistRepository:
        """Provide the catechist repository backed by the request session."""
        return SqlAlchemyCatechistRepository(session)
