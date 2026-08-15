from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from cms_common.health_check.handlers.health_check_handler import HealthCheckHandler
from cms_common.health_check.models.health_check_response import HealthCheckResponse

from containers import ApplicationContainer

router = APIRouter(tags=["health"])


@router.get("/ping")
@inject
async def ping(
    health_handler: HealthCheckHandler = Depends(
        Provide[ApplicationContainer.health_check_handler]
    ),
) -> HealthCheckResponse:
    return health_handler.get_health_status()
