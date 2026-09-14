from containers import ApplicationContainer
from controllers.auth_controller import router as auth_router
from controllers.health_controller import router as health_router
from controllers.study_year_controller import router as study_year_router
from controllers.schedule_activity_type_controller import router as schedule_activity_type_router
from cms_common.models import CmsAdminDashboardSettings
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware


def __custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


def create_app() -> FastAPI:
    settings = CmsAdminDashboardSettings()

    container = ApplicationContainer()
    container.config.from_pydantic(settings)
    container.wire()

    application = FastAPI(
        title="CMS Admin Dashboard API",
        version=settings.version,
        description="REST API for Admin Dashboard",
        generate_unique_id_function=__custom_generate_unique_id
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(health_router, prefix="/dashboard-api")
    application.include_router(auth_router, prefix="/dashboard-api")
    application.include_router(study_year_router, prefix="/dashboard-api")
    application.include_router(schedule_activity_type_router, prefix="/dashboard-api")
    return application
