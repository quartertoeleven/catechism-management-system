from cms_common.services.general_schedule_service_interface import (
    GeneralScheduleServiceInterface,
)
from cms_common.services.schedule_activity_type_service_interface import (
    ScheduleActivityTypeServiceInterface,
)
from cms_common.services.study_year_service_interface import StudyYearServiceInterface
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.upsert_general_schedule_request import UpsertGeneralScheduleRequest
from models.upsert_general_schedule_response import UpsertGeneralScheduleResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UpsertGeneralScheduleHandler(BaseAsyncHandler):
    def __init__(
        self,
        general_schedule_service: GeneralScheduleServiceInterface,
        study_year_service: StudyYearServiceInterface,
        schedule_activity_type_service: ScheduleActivityTypeServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._general_schedule_service = general_schedule_service
        self._study_year_service = study_year_service
        self._schedule_activity_type_service = schedule_activity_type_service
        self._session_factory = session_factory

    async def handle(
        self, body: UpsertGeneralScheduleRequest, translator: Translator
    ) -> UpsertGeneralScheduleResponse:
        async with self._session_factory() as session:
            activity_type = await self._schedule_activity_type_service.get_by_id(
                session, body.schedule_activity_type_id
            )
            if activity_type is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.schedule_activity_type_not_found"),
                )

            if body.id is not None:
                schedule = await self._general_schedule_service.get_by_id(
                    session, body.id
                )
                if schedule is None:
                    raise HTTPException(
                        status_code=404,
                        detail=translator.gettext("error.general_schedule_not_found"),
                    )
                schedule = await self._general_schedule_service.update(
                    session,
                    schedule,
                    schedule_activity_type_id=body.schedule_activity_type_id,
                    name=body.name,
                    start_at=body.start_at,
                    end_at=body.end_at,
                    detail=body.detail,
                    is_attendence_check=body.is_attendence_check,
                )
            else:
                if body.study_year_id is not None:
                    study_year = await self._study_year_service.get_by_id(
                        session, body.study_year_id
                    )
                    if study_year is None:
                        raise HTTPException(
                            status_code=404,
                            detail=translator.gettext("error.study_year_not_found"),
                        )
                    study_year_id = study_year.id
                else:
                    current = await self._study_year_service.get_current_active(session)
                    if current is None:
                        raise HTTPException(
                            status_code=404,
                            detail=translator.gettext("error.no_current_study_year"),
                        )
                    study_year_id = current.id

                schedule = await self._general_schedule_service.create(
                    session,
                    study_year_id=study_year_id,
                    schedule_activity_type_id=body.schedule_activity_type_id,
                    name=body.name,
                    start_at=body.start_at,
                    end_at=body.end_at,
                    detail=body.detail,
                    is_attendence_check=body.is_attendence_check,
                )

            await session.commit()
            await session.refresh(schedule)

        return UpsertGeneralScheduleResponse(
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
