from cms_common.services import ProfileService
from cms_integrations.logto import LogtoClientFactory, LogtoService
from cms_locale import LocaleConfig, LocaleService
from dependency_injector import containers, providers
from handlers.callback_handler import CallbackHandler
from handlers.check_handler import CheckHandler
from handlers.health_check_handler import HealthCheckHandler
from handlers.login_handler import LoginHandler
from handlers.logout_handler import LogoutHandler
from handlers.profile_handler import ProfileHandler
from services.auth_service import AuthService
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    locale_config = providers.Singleton(
        LocaleConfig,
        catalogs_dir=config.locale.catalogs_dir,
        default_locale=config.locale.default_locale,
        supported_locales=config.locale.supported_locales,
        fallback_locale=config.locale.fallback_locale,
    )

    locale_service = providers.Singleton(
        LocaleService,
        config=locale_config,
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

    logto_client_factory = providers.Singleton(
        LogtoClientFactory,
        endpoint=config.logto.endpoint,
        app_id=config.logto.app_id,
        app_secret=config.logto.app_secret,
    )

    logto_service = providers.Singleton(LogtoService)

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

    health_check_handler = providers.Singleton(
        HealthCheckHandler,
        version=config.version,
    )

    profile_service = providers.Singleton(
        ProfileService,
        logto_service=logto_service,
        session_factory=session_factory,
    )

    profile_handler = providers.Singleton(
        ProfileHandler,
        auth_service=auth_service,
        profile_service=profile_service,
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
            "dependencies.locale_dependency",
        ],
    )
