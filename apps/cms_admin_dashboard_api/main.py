import os
from pathlib import Path

from containers import ApplicationContainer
from controllers.auth_controller import router as auth_router
from controllers.health_controller import router as health_router
from controllers.study_year_controller import router as study_year_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    session_secret = os.getenv("AUTH_SESSION_SECRET", "")
    if not session_secret:
        raise RuntimeError("AUTH_SESSION_SECRET is required")

    container = ApplicationContainer()
    container.config.from_dict(
        {
            "version": os.getenv("CMS_VERSION", "0.1.0"),
            "logto": {
                "endpoint": os.getenv("CMS_ADMIN_DASHBOARD_LOGTO_ENDPOINT", ""),
                "app_id": os.getenv("CMS_ADMIN_DASHBOARD_LOGTO_APP_ID", ""),
                "app_secret": os.getenv("CMS_ADMIN_DASHBOARD_LOGTO_APP_SECRET", ""),
                "redirect_uri": os.getenv(
                    "CMS_ADMIN_DASHBOARD_LOGTO_REDIRECT_URI",
                    "http://localhost:8000/dashboard-api/auth/callback",
                ),
                "resources": [
                    resource.strip()
                    for resource in os.getenv(
                        "CMS_ADMIN_DASHBOARD_LOGTO_RESOURCES", ""
                    ).split(",")
                    if resource.strip()
                ],
            },
            "frontend_url": os.getenv(
                "CMS_ADMIN_DASHBOARD_FRONTEND_URL", "http://localhost:3000"
            ),
            "session_secret": session_secret,
            "database": {
                "url": os.getenv(
                    "DATABASE_URL",
                    "postgresql+psycopg://postgres:postgres@localhost:5432/catechism_management_system",
                ),
            },
            "cookie": {
                "name": os.getenv(
                    "CMS_ADMIN_DASHBOARD_SESSION_COOKIE_NAME", "cms_session"
                ),
                "secure": os.getenv("AUTH_SESSION_COOKIE_SECURE", "false").lower()
                == "true",
                "samesite": os.getenv("AUTH_SESSION_COOKIE_SAMESITE", "lax"),
                "max_age": int(os.getenv("AUTH_SESSION_COOKIE_MAX_AGE", "2592000")),
            },
            "locale": {
                "catalogs_dir": str(Path(__file__).resolve().parent / "translations"),
                "default_locale": "vi",
                "supported_locales": ["en", "vi"],
                "fallback_locale": "vi",
            },
        }
    )
    container.wire()

    application = FastAPI(
        title="CMS Admin Dashboard API",
        version="0.1.0",
        description="REST API for Admin Dashboard",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            origin.strip()
            for origin in os.getenv(
                "CMS_ADMIN_DASHBOARD_CORS_ORIGINS", "http://localhost:3000"
            ).split(",")
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(health_router, prefix="/dashboard-api")
    application.include_router(auth_router, prefix="/dashboard-api")
    application.include_router(study_year_router, prefix="/dashboard-api")
    return application
