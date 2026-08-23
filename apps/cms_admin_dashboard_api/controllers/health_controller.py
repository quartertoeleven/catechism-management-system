from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from handlers.health_check_handler import HealthCheckHandler
from models.health_check_response import HealthCheckResponse

router = APIRouter(tags=["health"])


@router.get("/ping")
@inject
async def ping(
    health_handler: HealthCheckHandler = Depends(
        Provide[ApplicationContainer.health_check_handler]
    ),
) -> HealthCheckResponse:
    return health_handler()
