from uuid import UUID

from cms_common.models import CatechistSchema
from cms_common.services.catechist_service import CatechistService
from cms_common.services.grade_service_interface import GradeServiceInterface
from cms_common.services.study_year_service_interface import (
    StudyYearServiceInterface,
)
from cms_db_models.directory.catechist import Catechist
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.get_grade_response import GetGradeResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


def _to_catechist_schema(catechist: Catechist | None) -> CatechistSchema | None:
    if catechist is None:
        return None
    return CatechistSchema(
        id=catechist.id,
        code=catechist.code,
        title=catechist.title,
        saint_name=catechist.saint_name,
        first_name=catechist.first_name,
        middle_name=catechist.middle_name,
        last_name=catechist.last_name,
        gender=catechist.gender,
    )


class GetGradeHandler(BaseAsyncHandler):
    def __init__(
        self,
        grade_service: GradeServiceInterface,
        study_year_service: StudyYearServiceInterface,
        catechist_service: CatechistService,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._grade_service = grade_service
        self._study_year_service = study_year_service
        self._catechist_service = catechist_service
        self._session_factory = session_factory

    async def handle(self, grade_id: UUID, translator: Translator) -> GetGradeResponse:
        async with self._session_factory() as session:
            grade = await self._grade_service.get_by_id(session, grade_id)
            if grade is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.grade_not_found"),
                )

            # Relationship load is not allowed in async session — fetch explicitly.
            study_year = await self._study_year_service.get_by_id(
                session, grade.study_year_id
            )
            if study_year is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.study_year_not_found"),
                )

            catechist_ids = [
                catechist_id
                for catechist_id in (
                    grade.leader_catechist_id,
                    grade.vice_leader_catechist_id,
                    grade.secretary_catechist_id,
                    grade.treasurer_catechist_id,
                )
                if catechist_id is not None
            ]
            catechists: dict[UUID, Catechist] = {}
            if catechist_ids:
                found = await self._catechist_service.list_by_ids(
                    session, catechist_ids
                )
                catechists = {catechist.id: catechist for catechist in found}

            def catechist_of(catechist_id: UUID | None) -> CatechistSchema | None:
                if catechist_id is None:
                    return None
                return _to_catechist_schema(catechists.get(catechist_id))

        return GetGradeResponse(
            id=grade.id,
            study_year_code=study_year.code,
            code=grade.code,
            name=grade.name,
            leader_catechist=catechist_of(grade.leader_catechist_id),
            vice_leader_catechist=catechist_of(grade.vice_leader_catechist_id),
            secretary_catechist=catechist_of(grade.secretary_catechist_id),
            treasurer_catechist=catechist_of(grade.treasurer_catechist_id),
            created=grade.created,
            updated=grade.updated,
        )
