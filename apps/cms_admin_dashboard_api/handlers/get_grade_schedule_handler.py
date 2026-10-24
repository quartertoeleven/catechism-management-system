from uuid import UUID

from cms_common.services.grade_schedule_service_interface import (
    GradeScheduleServiceInterface,
)
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.get_grade_schedule_response import GetGradeScheduleResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class GetGradeScheduleHandler(BaseAsyncHandler):
    def __init__(
        self,
        grade_schedule_service: GradeScheduleServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._grade_schedule_service = grade_schedule_service
        self._session_factory = session_factory

    async def handle(
        self, schedule_id: UUID, translator: Translator
    ) -> GetGradeScheduleResponse:
        async with self._session_factory() as session:
            schedule = await self._grade_schedule_service.get_by_id(
                session, schedule_id
            )
            if schedule is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.grade_schedule_not_found"),
                )

        return GetGradeScheduleResponse(
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
