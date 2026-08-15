from dependency_injector import containers, providers

from cms_common.integrations.logto import LogtoAuthClient
from cms_common.profile import ProfileHandler, ProfileService
from cms_db_models.containers import DBContainer


class CommonContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    logto_auth_client = providers.Singleton(
        LogtoAuthClient,
        endpoint=config.logto.endpoint,
        app_id=config.logto.app_id,
        app_secret=config.logto.app_secret,
    )

    db = providers.Container(
        DBContainer,
        config=config,
    )

    profile_service = providers.Singleton(
        ProfileService,
        logto_auth_client=logto_auth_client,
        session_factory=db.session_factory,
    )

    profile_handler = providers.Singleton(
        ProfileHandler,
        profile_service=profile_service,
    )
