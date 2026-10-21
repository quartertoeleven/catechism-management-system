from uuid import UUID

from cms_locale import Translator
from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response
from handlers.delete_general_schedule_handler import DeleteGeneralScheduleHandler
from handlers.get_general_schedule_handler import GetGeneralScheduleHandler
from handlers.list_general_schedules_handler import ListGeneralSchedulesHandler
from handlers.upsert_general_schedule_handler import UpsertGeneralScheduleHandler
from logto import IdTokenClaims
from models.get_general_schedule_response import GetGeneralScheduleResponse
from models.list_general_schedules_response import ListGeneralSchedulesResponse
from models.upsert_general_schedule_request import UpsertGeneralScheduleRequest
from models.upsert_general_schedule_response import UpsertGeneralScheduleResponse

from dependencies.auth_dependency import get_authenticated_user
from dependencies.locale_dependency import get_locale_translator

router = APIRouter(prefix="/general-schedules", tags=["general-schedules"])


@router.get("")
@inject
async def list_general_schedules(
    study_year_id: UUID | None = Query(default=None),
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: ListGeneralSchedulesHandler = Depends(
        Provide[ApplicationContainer.list_general_schedules_handler]
    ),
) -> ListGeneralSchedulesResponse:
    return await handler(study_year_id, translator)


@router.get("/{schedule_id}")
@inject
async def get_general_schedule(
    schedule_id: UUID,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: GetGeneralScheduleHandler = Depends(
        Provide[ApplicationContainer.get_general_schedule_handler]
    ),
) -> GetGeneralScheduleResponse:
    return await handler(schedule_id, translator)


@router.delete("/{schedule_id}")
@inject
async def delete_general_schedule(
    schedule_id: UUID,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: DeleteGeneralScheduleHandler = Depends(
        Provide[ApplicationContainer.delete_general_schedule_handler]
    ),
) -> Response:
    return await handler(schedule_id, translator)


@router.post("")
@inject
async def upsert_general_schedule(
    body: UpsertGeneralScheduleRequest,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: UpsertGeneralScheduleHandler = Depends(
        Provide[ApplicationContainer.upsert_general_schedule_handler]
    ),
) -> UpsertGeneralScheduleResponse:
    return await handler(body, translator)
