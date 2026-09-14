from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from handlers.list_schedule_activity_types_handler import (
    ListScheduleActivityTypesHandler,
)
from logto import IdTokenClaims
from models.list_schedule_activity_types_response import (
    ListScheduleActivityTypesResponse,
)

from dependencies.auth_dependency import get_authenticated_user

router = APIRouter(
    prefix="/schedule-activity-types", tags=["schedule-activity-types"]
)


@router.get("/")
@inject
async def list_schedule_activity_types(
    claims: IdTokenClaims = Depends(get_authenticated_user),
    handler: ListScheduleActivityTypesHandler = Depends(
        Provide[ApplicationContainer.list_schedule_activity_types_handler]
    ),
) -> ListScheduleActivityTypesResponse:
    return await handler()
