from uuid import UUID

from cms_common.services.general_schedule_service_interface import (
    GeneralScheduleServiceInterface,
)
from cms_common.services.study_year_service_interface import StudyYearServiceInterface
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.list_general_schedules_response import (
    GeneralScheduleListItem,
    ListGeneralSchedulesResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class ListGeneralSchedulesHandler(BaseAsyncHandler):
    def __init__(
        self,
        general_schedule_service: GeneralScheduleServiceInterface,
        study_year_service: StudyYearServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._general_schedule_service = general_schedule_service
        self._study_year_service = study_year_service
        self._session_factory = session_factory

    async def handle(
        self, study_year_id: UUID | None, translator: Translator
    ) -> ListGeneralSchedulesResponse:
        async with self._session_factory() as session:
            if study_year_id is None:
                current = await self._study_year_service.get_current_active(session)
                if current is None:
                    raise HTTPException(
                        status_code=404,
                        detail=translator.gettext("error.no_current_study_year"),
                    )
                study_year_id = current.id

            schedules = await self._general_schedule_service.list_by_study_year(
                session, study_year_id
            )

        return ListGeneralSchedulesResponse(
            data=[
                GeneralScheduleListItem(
                    id=schedule.id,
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
