from cms_common.services.grade_schedule_service_interface import (
    GradeScheduleServiceInterface,
)
from cms_common.services.grade_service_interface import GradeServiceInterface
from cms_common.services.general_schedule_service_interface import (
    GeneralScheduleServiceInterface,
)
from cms_common.services.schedule_activity_type_service_interface import (
    ScheduleActivityTypeServiceInterface,
)
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.upsert_grade_schedule_request import UpsertGradeScheduleRequest
from models.upsert_grade_schedule_response import UpsertGradeScheduleResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UpsertGradeScheduleHandler(BaseAsyncHandler):
    def __init__(
        self,
        grade_schedule_service: GradeScheduleServiceInterface,
        grade_service: GradeServiceInterface,
        general_schedule_service: GeneralScheduleServiceInterface,
        schedule_activity_type_service: ScheduleActivityTypeServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._grade_schedule_service = grade_schedule_service
        self._grade_service = grade_service
        self._general_schedule_service = general_schedule_service
        self._schedule_activity_type_service = schedule_activity_type_service
        self._session_factory = session_factory

    async def handle(
        self, body: UpsertGradeScheduleRequest, translator: Translator
    ) -> UpsertGradeScheduleResponse:
        async with self._session_factory() as session:
            activity_type = await self._schedule_activity_type_service.get_by_id(
                session, body.schedule_activity_type_id
            )
            if activity_type is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.schedule_activity_type_not_found"),
                )

            grade = await self._grade_service.get_by_id(session, body.grade_id)
            if grade is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.grade_not_found"),
                )

            if body.general_schedule_id is not None:
                general_schedule = await self._general_schedule_service.get_by_id(
                    session, body.general_schedule_id
                )
                if general_schedule is None:
                    raise HTTPException(
                        status_code=404,
                        detail=translator.gettext("error.general_schedule_not_found"),
                    )

            if body.id is not None:
                schedule = await self._grade_schedule_service.get_by_id(
                    session, body.id
                )
                if schedule is None:
                    raise HTTPException(
                        status_code=404,
                        detail=translator.gettext("error.grade_schedule_not_found"),
                    )
                schedule = await self._grade_schedule_service.update(
                    session,
                    schedule,
                    general_schedule_id=body.general_schedule_id,
                    schedule_activity_type_id=body.schedule_activity_type_id,
                    name=body.name,
                    start_at=body.start_at,
                    end_at=body.end_at,
                    detail=body.detail,
                    is_attendence_check=body.is_attendence_check,
                )
            else:
                schedule = await self._grade_schedule_service.create(
                    session,
                    study_year_id=grade.study_year_id,
                    grade_id=grade.id,
                    general_schedule_id=body.general_schedule_id,
                    schedule_activity_type_id=body.schedule_activity_type_id,
                    name=body.name,
                    start_at=body.start_at,
                    end_at=body.end_at,
                    detail=body.detail,
                    is_attendence_check=body.is_attendence_check,
                )

            await session.commit()
            await session.refresh(schedule)

        return UpsertGradeScheduleResponse(
            id=schedule.id,
            study_year_id=schedule.study_year_id,
            grade_id=schedule.grade_id,
            general_schedule_id=schedule.general_schedule_id,
            schedule_activity_type_id=schedule.schedule_activity_type_id,
            name=schedule.name,
            start_at=schedule.start_at,
            end_at=schedule.end_at,
            detail=schedule.detail,
            is_attendence_check=schedule.is_attendence_check,
            created=schedule.created,
            updated=schedule.updated,
        )
