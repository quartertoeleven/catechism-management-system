from uuid import UUID

from cms_common.services.grade_schedule_service_interface import (
    GradeScheduleServiceInterface,
)
from cms_common.services.grade_service_interface import GradeServiceInterface
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.list_grade_schedules_response import (
    GradeScheduleListItem,
    ListGradeSchedulesResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class ListGradeSchedulesHandler(BaseAsyncHandler):
    def __init__(
        self,
        grade_schedule_service: GradeScheduleServiceInterface,
        grade_service: GradeServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._grade_schedule_service = grade_schedule_service
        self._grade_service = grade_service
        self._session_factory = session_factory

    async def handle(
        self, grade_id: UUID, translator: Translator
    ) -> ListGradeSchedulesResponse:
        async with self._session_factory() as session:
            grade = await self._grade_service.get_by_id(session, grade_id)
            if grade is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.grade_not_found"),
                )

            schedules = await self._grade_schedule_service.list_by_grade(
                session, grade_id
            )

        return ListGradeSchedulesResponse(
            data=[
                GradeScheduleListItem(
                    id=schedule.id,
                    grade_id=schedule.grade_id,
                    general_schedule_id=schedule.general_schedule_id,
                    schedule_activity_type_id=schedule.schedule_activity_type_id,
                    schedule_activity_type_name=schedule.schedule_activity_type.name,
                    schedule_activity_type_color=schedule.schedule_activity_type.color,
                    name=schedule.name,
                    start_at=schedule.start_at,
                    end_at=schedule.end_at,
                    detail=schedule.detail,
                    is_attendence_check=schedule.is_attendence_check,
                    updated=schedule.updated,
                )
                for schedule in schedules
            ]
        )
