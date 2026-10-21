from cms_common.services.study_year_service_interface import (
    StudyYearServiceInterface,
)
from handlers.base_handler import BaseAsyncHandler
from models.app_state_response import AppStateResponse, StudyYearInfo
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class AppStateHandler(BaseAsyncHandler):
    def __init__(
        self,
        study_year_service: StudyYearServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._study_year_service = study_year_service
        self._session_factory = session_factory

    async def handle(self) -> AppStateResponse:
        async with self._session_factory() as session:
            current = await self._study_year_service.get_current_active(session)

        return AppStateResponse(
            current_selected_study_year=StudyYearInfo(
                id=current.id,
                code=current.code,
                name=current.name,
            )
            if current
            else None
        )
