from uuid import UUID

from cms_common.services.general_schedule_service_interface import (
    GeneralScheduleServiceInterface,
)
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.get_general_schedule_response import GetGeneralScheduleResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class GetGeneralScheduleHandler(BaseAsyncHandler):
    def __init__(
        self,
        general_schedule_service: GeneralScheduleServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._general_schedule_service = general_schedule_service
        self._session_factory = session_factory

    async def handle(
        self, schedule_id: UUID, translator: Translator
    ) -> GetGeneralScheduleResponse:
        async with self._session_factory() as session:
            schedule = await self._general_schedule_service.get_by_id(
                session, schedule_id
            )
            if schedule is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.general_schedule_not_found"),
                )

        return GetGeneralScheduleResponse(
            id=schedule.id,
            study_year_id=schedule.study_year_id,
            schedule_activity_type_id=schedule.schedule_activity_type_id,
            name=schedule.name,
            start_at=schedule.start_at,
            end_at=schedule.end_at,
            detail=schedule.detail,
            is_attendence_check=schedule.is_attendence_check,
            created=schedule.created,
            updated=schedule.updated,
        )
