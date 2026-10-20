from uuid import UUID

from cms_common.services.general_schedule_service_interface import (
    GeneralScheduleServiceInterface,
)
from cms_locale import Translator
from fastapi import HTTPException, Response
from handlers.base_handler import BaseAsyncHandler
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DeleteGeneralScheduleHandler(BaseAsyncHandler):
    def __init__(
        self,
        general_schedule_service: GeneralScheduleServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._general_schedule_service = general_schedule_service
        self._session_factory = session_factory

    async def handle(self, schedule_id: UUID, translator: Translator) -> Response:
        async with self._session_factory() as session:
            schedule = await self._general_schedule_service.get_by_id(
                session, schedule_id
            )
            if schedule is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.general_schedule_not_found"),
                )
            await self._general_schedule_service.delete(session, schedule)
            await session.commit()

        return Response(status_code=204)
