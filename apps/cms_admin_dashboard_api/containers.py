from cms_common.models import CmsAdminDashboardSettings
from cms_common.services import (
    CatechistService,
    ProfileService,
    StudyYearService,
    ScheduleActivityTypeService,
    GeneralScheduleService,
    GradeScheduleService,
    GradeService,
)
from cms_integrations.logto import (
    JwtVerificationService,
    LogtoClientFactory,
    LogtoService,
)
from cms_locale import LocaleConfig, LocaleService
from dependency_injector import containers, providers
from handlers.callback_handler import CallbackHandler
from handlers.app_state_handler import AppStateHandler
from handlers.check_handler import CheckHandler
from handlers.health_check_handler import HealthCheckHandler
from handlers.login_handler import LoginHandler
from handlers.logout_handler import LogoutHandler
from handlers.create_study_year_handler import CreateStudyYearHandler
from handlers.list_study_years_handler import ListStudyYearsHandler
from handlers.list_schedule_activity_types_handler import (
    ListScheduleActivityTypesHandler,
)
from handlers.list_general_schedules_handler import ListGeneralSchedulesHandler
from handlers.list_grades_handler import ListGradesHandler
from handlers.create_grade_handler import CreateGradeHandler
from handlers.get_grade_handler import GetGradeHandler
from handlers.update_grade_handler import UpdateGradeHandler
from handlers.delete_grade_handler import DeleteGradeHandler
from handlers.list_catechists_handler import ListCatechistsHandler
from handlers.delete_general_schedule_handler import DeleteGeneralScheduleHandler
from handlers.delete_grade_schedule_handler import DeleteGradeScheduleHandler
from handlers.get_general_schedule_handler import GetGeneralScheduleHandler
from handlers.get_grade_schedule_handler import GetGradeScheduleHandler
from handlers.list_grade_schedules_handler import ListGradeSchedulesHandler
from handlers.sync_grade_schedule_handler import SyncGradeScheduleHandler
from handlers.upsert_general_schedule_handler import UpsertGeneralScheduleHandler
from handlers.upsert_grade_schedule_handler import UpsertGradeScheduleHandler
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

    schedule_activity_type_service = providers.Singleton(ScheduleActivityTypeService)

    general_schedule_service = providers.Singleton(GeneralScheduleService)

    grade_service = providers.Singleton(GradeService)

    grade_schedule_service = providers.Singleton(GradeScheduleService)

    catechist_service = providers.Singleton(CatechistService)

    list_grade_schedules_handler = providers.Singleton(
        ListGradeSchedulesHandler,
        grade_schedule_service=grade_schedule_service,
        grade_service=grade_service,
        session_factory=session_factory,
    )

    get_grade_schedule_handler = providers.Singleton(
        GetGradeScheduleHandler,
        grade_schedule_service=grade_schedule_service,
        session_factory=session_factory,
    )

    delete_grade_schedule_handler = providers.Singleton(
        DeleteGradeScheduleHandler,
        grade_schedule_service=grade_schedule_service,
        session_factory=session_factory,
    )

    upsert_grade_schedule_handler = providers.Singleton(
        UpsertGradeScheduleHandler,
        grade_schedule_service=grade_schedule_service,
        grade_service=grade_service,
        general_schedule_service=general_schedule_service,
        schedule_activity_type_service=schedule_activity_type_service,
        session_factory=session_factory,
    )

    sync_grade_schedule_handler = providers.Singleton(
        SyncGradeScheduleHandler,
        grade_schedule_service=grade_schedule_service,
        grade_service=grade_service,
        general_schedule_service=general_schedule_service,
        session_factory=session_factory,
    )

    upsert_general_schedule_handler = providers.Singleton(
        UpsertGeneralScheduleHandler,
        general_schedule_service=general_schedule_service,
        study_year_service=study_year_service,
        schedule_activity_type_service=schedule_activity_type_service,
        session_factory=session_factory,
    )

    get_general_schedule_handler = providers.Singleton(
        GetGeneralScheduleHandler,
        general_schedule_service=general_schedule_service,
        session_factory=session_factory,
    )

    delete_general_schedule_handler = providers.Singleton(
        DeleteGeneralScheduleHandler,
        general_schedule_service=general_schedule_service,
        session_factory=session_factory,
    )

    list_general_schedules_handler = providers.Singleton(
        ListGeneralSchedulesHandler,
        general_schedule_service=general_schedule_service,
        study_year_service=study_year_service,
        session_factory=session_factory,
    )

    create_study_year_handler = providers.Singleton(
        CreateStudyYearHandler,
        study_year_service=study_year_service,
        session_factory=session_factory,
    )

    list_study_years_handler = providers.Singleton(
        ListStudyYearsHandler,
        study_year_service=study_year_service,
        session_factory=session_factory,
    )

    list_schedule_activity_types_handler = providers.Singleton(
        ListScheduleActivityTypesHandler,
        schedule_activity_type_service=schedule_activity_type_service,
        session_factory=session_factory,
    )

    list_grades_handler = providers.Singleton(
        ListGradesHandler,
        grade_service=grade_service,
        study_year_service=study_year_service,
        session_factory=session_factory,
    )

    create_grade_handler = providers.Singleton(
        CreateGradeHandler,
        grade_service=grade_service,
        study_year_service=study_year_service,
        catechist_service=catechist_service,
        session_factory=session_factory,
    )

    list_catechists_handler = providers.Singleton(
        ListCatechistsHandler,
        catechist_service=catechist_service,
        session_factory=session_factory,
    )

    get_grade_handler = providers.Singleton(
        GetGradeHandler,
        grade_service=grade_service,
        study_year_service=study_year_service,
        catechist_service=catechist_service,
        session_factory=session_factory,
    )

    update_grade_handler = providers.Singleton(
        UpdateGradeHandler,
        grade_service=grade_service,
        catechist_service=catechist_service,
        session_factory=session_factory,
    )

    delete_grade_handler = providers.Singleton(
        DeleteGradeHandler,
        grade_service=grade_service,
        session_factory=session_factory,
    )

    app_state_handler = providers.Singleton(
        AppStateHandler,
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
            "controllers.schedule_activity_type_controller",
            "controllers.general_schedule_controller",
            "controllers.grade_schedule_controller",
            "controllers.grade_controller",
            "controllers.catechist_controller",
            "controllers.app_state_controller",
            "dependencies.auth_dependency",
            "dependencies.locale_dependency",
        ],
    )
