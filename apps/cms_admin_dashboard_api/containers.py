from dependency_injector import containers, providers

from cms_common.containers import CommonContainer

from services.auth_service import AuthService
from services.health_service import HealthService


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    common = providers.Container(CommonContainer)

    health_service = providers.Singleton(
        HealthService,
        version=config.version,
    )

    auth_service = providers.Singleton(
        AuthService,
        logto_auth_client=common.logto_auth_client,
        logto_redirect_uri=config.logto.redirect_uri,
        frontend_url=config.frontend_url,
        session_secret=config.session_secret,
        cookie_name=config.cookie.name,
        cookie_secure=config.cookie.secure,
        cookie_samesite=config.cookie.samesite,
        cookie_max_age=config.cookie.max_age,
    )

    wiring_config = containers.WiringConfiguration(
        modules=[
            "controllers.health_controller",
            "controllers.auth_controller",
            "dependencies.auth",
        ],
    )
