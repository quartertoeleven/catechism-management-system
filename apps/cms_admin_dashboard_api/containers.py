from cms_common.models import CmsAdminDashboardSettings
from cms_common.services import ProfileService, StudyYearService
from cms_integrations.logto import (
    JwtVerificationService,
    LogtoClientFactory,
    LogtoService,
)
from cms_locale import LocaleConfig, LocaleService
from dependency_injector import containers, providers
from handlers.callback_handler import CallbackHandler
from handlers.check_handler import CheckHandler
from handlers.health_check_handler import HealthCheckHandler
from handlers.login_handler import LoginHandler
from handlers.logout_handler import LogoutHandler
from handlers.create_study_year_handler import CreateStudyYearHandler
from handlers.profile_handler import ProfileHandler
from services.auth_service import AuthService
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    locale_config = providers.Singleton(
        LocaleConfig,
        catalogs_dir=config.locale_catalogs_dir,
        default_locale=config.locale_default_locale,
        supported_locales=config.locale_supported_locales,
        fallback_locale=config.locale_fallback_locale,
    )

    locale_service = providers.Singleton(
        LocaleService,
        config=locale_config,
    )

    database_engine = providers.Singleton(
        create_async_engine,
        config.common.database_url,
    )

    session_factory = providers.Singleton(
        async_sessionmaker,
        database_engine,
        expire_on_commit=False,
    )

    logto_client_factory = providers.Singleton(
        LogtoClientFactory,
        endpoint=config.logto_endpoint,
        app_id=config.logto_app_id,
        app_secret=config.logto_app_secret,
        resources=config.logto_resources,
    )

    jwt_verification_service = providers.Singleton(
        JwtVerificationService,
        endpoint=config.logto_endpoint,
        app_id=config.logto_app_id,
    )

    logto_service = providers.Singleton(
        LogtoService,
        jwt_verification_service=jwt_verification_service,
    )

    auth_service = providers.Singleton(
        AuthService,
        logto_client_factory=logto_client_factory,
        logto_service=logto_service,
        logto_redirect_uri=config.logto_redirect_uri,
        frontend_url=config.frontend_url,
        session_secret=config.common.session_secret,
        cookie_name=config.common.cookie_name,
        cookie_secure=config.common.cookie_secure,
        cookie_samesite=config.common.cookie_samesite,
        cookie_max_age=config.common.cookie_max_age,
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

    study_year_service = providers.Singleton(StudyYearService)

    create_study_year_handler = providers.Singleton(
        CreateStudyYearHandler,
        study_year_service=study_year_service,
        session_factory=session_factory,
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
            "controllers.study_year_controller",
            "dependencies.auth_dependency",
            "dependencies.locale_dependency",
        ],
    )
