from fastapi import FastAPI

from containers import ApplicationContainer
from controllers.health_controller import router as health_router


def create_app() -> FastAPI:
    container = ApplicationContainer()
    container.config.from_dict({"version": "0.1.0"})
    container.wire()

    application = FastAPI(
        title="CMS Admin Dashboard API",
        version="0.1.0",
        description="REST API for Admin Dashboard",
    )
    application.container = container
    application.include_router(health_router)
    return application
