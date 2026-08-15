from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from cms_common.integrations.logto import LogtoAuthClient
from cms_common.profile import ProfileHandler


class CommonContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logto_auth_client = providers.Singleton(
        LogtoAuthClient,
        endpoint=config.logto.endpoint,
        app_id=config.logto.app_id,
        app_secret=config.logto.app_secret,
    )

    database_engine = providers.Singleton(
        create_async_engine,
        config.database.url,
    )

    session_factory = providers.Singleton(
        async_sessionmaker,
        database_engine,
        expire_on_commit=False,
    )

    profile_handler = providers.Singleton(
        ProfileHandler,
        logto_auth_client=logto_auth_client,
        session_factory=session_factory,
    )
