"""Admin dashboard REST API application."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Final

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from admin_dashboard_api.container import create_container
from admin_dashboard_api.controllers import health_router

API_TITLE: Final[str] = "Admin Dashboard API"
API_VERSION: Final[str] = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Release the dependency injection container when the app stops."""
    yield
    container: AsyncContainer = app.state.dishka_container
    await container.close()


def create_app() -> FastAPI:
    """Build the Admin Dashboard API application."""
    app = FastAPI(title=API_TITLE, version=API_VERSION, lifespan=lifespan)
    setup_dishka(create_container(), app)
    app.include_router(health_router)
    return app


app = create_app()
