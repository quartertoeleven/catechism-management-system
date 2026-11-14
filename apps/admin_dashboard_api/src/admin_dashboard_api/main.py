from typing import Final, Literal

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

API_TITLE: Final[str] = "Admin Dashboard API"
API_VERSION: Final[str] = "0.1.0"
HEALTH_PATH: Final[str] = "/health"
STATUS_OK: Final = "ok"

router = APIRouter()


class HealthResponse(BaseModel):
    status: Literal["ok"]


@router.get(HEALTH_PATH, response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status=STATUS_OK)


def create_app() -> FastAPI:
    app = FastAPI(title=API_TITLE, version=API_VERSION)
    app.include_router(router)
    return app


app = create_app()
