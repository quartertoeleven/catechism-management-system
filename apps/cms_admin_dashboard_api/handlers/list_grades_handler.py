from cms_common.services.grade_service_interface import GradeServiceInterface
from cms_common.services.study_year_service_interface import (
    StudyYearServiceInterface,
)
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.list_grades_response import GradeListItem, ListGradesResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class ListGradesHandler(BaseAsyncHandler):
    def __init__(
        self,
        grade_service: GradeServiceInterface,
        study_year_service: StudyYearServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._grade_service = grade_service
        self._study_year_service = study_year_service
        self._session_factory = session_factory

    async def handle(
        self, study_year_code: str | None, translator: Translator
    ) -> ListGradesResponse:
        async with self._session_factory() as session:
            if study_year_code is not None:
                study_year = await self._study_year_service.get_by_code(
                    session, study_year_code
                )
                if study_year is None:
                    raise HTTPException(
                        status_code=404,
                        detail=translator.gettext("error.study_year_not_found"),
                    )
            else:
                study_year = await self._study_year_service.get_current_active(session)
                if study_year is None:
                    raise HTTPException(
                        status_code=404,
                        detail=translator.gettext("error.no_current_study_year"),
                    )

            grades = await self._grade_service.list_by_study_year(
                session, study_year.id
            )

        return ListGradesResponse(
            data=[
                GradeListItem(
                    id=grade.id,
                    code=grade.code,
                    name=grade.name,
                )
                for grade in grades
            ]
        )
