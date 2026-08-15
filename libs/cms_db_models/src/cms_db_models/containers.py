from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class DBContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    database_engine = providers.Singleton(
        create_async_engine,
        config.database.url,
    )

    session_factory = providers.Singleton(
        async_sessionmaker,
        database_engine,
        expire_on_commit=False,
    )
