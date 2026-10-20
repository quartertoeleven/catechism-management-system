from cms_common.services.study_year_service_interface import StudyYearServiceInterface
from handlers.base_handler import BaseAsyncHandler
from models.list_study_years_response import ListStudyYearsResponse, StudyYearListItem
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class ListStudyYearsHandler(BaseAsyncHandler):
    def __init__(
        self,
        study_year_service: StudyYearServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._study_year_service = study_year_service
        self._session_factory = session_factory

    async def handle(self) -> ListStudyYearsResponse:
        async with self._session_factory() as session:
            study_years = await self._study_year_service.list_all(session)

        return ListStudyYearsResponse(
            data=[
                StudyYearListItem(
                    id=sy.id,
                    code=sy.code,
                    name=sy.name,
                    is_current=sy.is_current,
                    is_readonly=sy.is_readonly,
                )
                for sy in study_years
            ]
        )
