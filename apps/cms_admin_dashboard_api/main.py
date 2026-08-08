import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from containers import ApplicationContainer
from controllers.auth_controller import router as auth_router
from controllers.health_controller import router as health_router


def create_app() -> FastAPI:
    session_secret = os.getenv("SESSION_SECRET", "")
    if not session_secret:
        raise RuntimeError("SESSION_SECRET is required")

    container = ApplicationContainer()
    container.config.from_dict(
        {
            "version": os.getenv("CMS_VERSION", "0.1.0"),
            "logto": {
                "endpoint": os.getenv("LOGTO_ENDPOINT", ""),
                "app_id": os.getenv("LOGTO_APP_ID", ""),
                "app_secret": os.getenv("LOGTO_APP_SECRET", ""),
                "redirect_uri": os.getenv(
                    "LOGTO_REDIRECT_URI", "http://localhost:8000/auth/callback"
                ),
            },
            "frontend_url": os.getenv("FRONTEND_URL", "http://localhost:3000"),
            "session_secret": session_secret,
            "cookie": {
                "name": os.getenv("SESSION_COOKIE_NAME", "cms_session"),
                "secure": os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true",
                "samesite": os.getenv("SESSION_COOKIE_SAMESITE", "lax"),
                "max_age": int(os.getenv("SESSION_COOKIE_MAX_AGE", "2592000")),
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
            for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(health_router)
    application.include_router(auth_router)
    return application
