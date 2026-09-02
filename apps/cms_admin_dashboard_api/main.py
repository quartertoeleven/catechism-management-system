from containers import ApplicationContainer
from controllers.auth_controller import router as auth_router
from controllers.health_controller import router as health_router
from controllers.study_year_controller import router as study_year_router
from cms_common.models import CmsAdminDashboardSettings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    settings = CmsAdminDashboardSettings()

    container = ApplicationContainer()
    container.config.from_pydantic(settings)
    container.wire()

    application = FastAPI(
        title="CMS Admin Dashboard API",
        version=settings.version,
        description="REST API for Admin Dashboard",
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
    return application
