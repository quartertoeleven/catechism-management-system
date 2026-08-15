from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from cms_common.health_check.handlers.health_check_handler import HealthCheckHandler
from cms_common.health_check.services.health_service import HealthService
from cms_common.profile import ProfileHandler, ProfileService
from cms_integrations.logto import LogtoClientFactory, LogtoService

from handlers.login_handler import LoginHandler
from handlers.callback_handler import CallbackHandler
from handlers.logout_handler import LogoutHandler
from handlers.check_handler import CheckHandler
from services.auth_service import AuthService


class ApplicationContainer(containers.DeclarativeContainer):
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

    logto_client_factory = providers.Singleton(
        LogtoClientFactory,
        endpoint=config.logto.endpoint,
        app_id=config.logto.app_id,
        app_secret=config.logto.app_secret,
    )

    logto_service = providers.Singleton(LogtoService)

    health_service = providers.Singleton(
        HealthService,
        version=config.version,
    )

    health_check_handler = providers.Singleton(
        HealthCheckHandler,
        health_service=health_service,
    )

    profile_service = providers.Singleton(
        ProfileService,
        logto_service=logto_service,
        session_factory=session_factory,
    )

    profile_handler = providers.Singleton(
        ProfileHandler,
        profile_service=profile_service,
    )

    auth_service = providers.Singleton(
        AuthService,
        logto_client_factory=logto_client_factory,
        logto_service=logto_service,
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
