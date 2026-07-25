from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from containers import ApplicationContainer
from services.health_service import HealthService

router = APIRouter(tags=["health"])


@router.get("/ping")
@inject
async def ping(
    health_service: HealthService = Depends(
        Provide[ApplicationContainer.health_service]
    ),
):
    return health_service.get_health_status()
