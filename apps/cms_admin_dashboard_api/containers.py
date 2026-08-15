from dependency_injector import containers, providers

from cms_common.containers import CommonContainer
from cms_common.health_check.handlers.health_check_handler import HealthCheckHandler
from cms_common.health_check.services.health_service import HealthService

from services.auth_service import AuthService
from handlers.login_handler import LoginHandler
from handlers.callback_handler import CallbackHandler
from handlers.logout_handler import LogoutHandler
from handlers.check_handler import CheckHandler


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    common = providers.Container(CommonContainer)

    health_service = providers.Singleton(
        HealthService,
        version=config.version,
    )

    health_check_handler = providers.Singleton(
        HealthCheckHandler,
        health_service=health_service,
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

    login_handler = providers.Singleton(
        LoginHandler,
        auth_service=auth_service,
    )

    callback_handler = providers.Singleton(
        CallbackHandler,
        auth_service=auth_service,
    )

    logout_handler = providers.Singleton(
        LogoutHandler,
        auth_service=auth_service,
    )

    check_handler = providers.Singleton(
        CheckHandler,
        auth_service=auth_service,
    )

    wiring_config = containers.WiringConfiguration(
        modules=[
            "controllers.health_controller",
            "controllers.auth_controller",
        ],
    )
