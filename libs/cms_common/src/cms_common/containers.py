from dependency_injector import containers, providers

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

    profile_handler = providers.Singleton(
        ProfileHandler, logto_auth_client=logto_auth_client
    )