from uuid import UUID

from cms_locale import Translator
from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response
from handlers.delete_grade_schedule_handler import DeleteGradeScheduleHandler
from handlers.get_grade_schedule_handler import GetGradeScheduleHandler
from handlers.list_grade_schedules_handler import ListGradeSchedulesHandler
from handlers.sync_grade_schedule_handler import SyncGradeScheduleHandler
from handlers.upsert_grade_schedule_handler import UpsertGradeScheduleHandler
from logto import IdTokenClaims
from models.get_grade_schedule_response import GetGradeScheduleResponse
from models.list_grade_schedules_response import ListGradeSchedulesResponse
from models.sync_grade_schedule_request import SyncGradeScheduleRequest
from models.sync_grade_schedule_response import SyncGradeScheduleResponse
from models.upsert_grade_schedule_request import UpsertGradeScheduleRequest
from models.upsert_grade_schedule_response import UpsertGradeScheduleResponse

from dependencies.auth_dependency import get_authenticated_user
from dependencies.locale_dependency import get_locale_translator

router = APIRouter(prefix="/grade-schedules", tags=["grade-schedules"])


@router.get("")
@inject
async def list_grade_schedules(
    grade_id: UUID = Query(...),
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: ListGradeSchedulesHandler = Depends(
        Provide[ApplicationContainer.list_grade_schedules_handler]
    ),
) -> ListGradeSchedulesResponse:
    return await handler(grade_id, translator)


@router.get("/{schedule_id}")
@inject
async def get_grade_schedule(
    schedule_id: UUID,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: GetGradeScheduleHandler = Depends(
        Provide[ApplicationContainer.get_grade_schedule_handler]
    ),
) -> GetGradeScheduleResponse:
    return await handler(schedule_id, translator)


@router.delete("/{schedule_id}")
@inject
async def delete_grade_schedule(
    schedule_id: UUID,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: DeleteGradeScheduleHandler = Depends(
        Provide[ApplicationContainer.delete_grade_schedule_handler]
    ),
) -> Response:
    return await handler(schedule_id, translator)


@router.post("/sync")
@inject
async def sync_grade_schedules(
    body: SyncGradeScheduleRequest,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: SyncGradeScheduleHandler = Depends(
        Provide[ApplicationContainer.sync_grade_schedule_handler]
    ),
) -> SyncGradeScheduleResponse:
    return await handler(body, translator)


@router.post("")
@inject
async def upsert_grade_schedule(
    body: UpsertGradeScheduleRequest,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: UpsertGradeScheduleHandler = Depends(
        Provide[ApplicationContainer.upsert_grade_schedule_handler]
    ),
) -> UpsertGradeScheduleResponse:
    return await handler(body, translator)
