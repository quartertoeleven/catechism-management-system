from uuid import UUID

from cms_common.services.catechist_service import CatechistService
from cms_common.services.grade_service_interface import GradeServiceInterface
from cms_common.services.study_year_service_interface import (
    StudyYearServiceInterface,
)
from cms_db_models.study_year.grade import (
    GRADE_CODE_MAX_LENGTH,
    GRADE_NAME_MAX_LENGTH,
)
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.create_grade_request import CreateGradeRequest
from models.create_grade_response import CreateGradeResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class CreateGradeHandler(BaseAsyncHandler):
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

    async def handle(
        self, body: CreateGradeRequest, translator: Translator
    ) -> CreateGradeResponse:
        async with self._session_factory() as session:
            study_year = await self._study_year_service.get_by_code(
                session, body.study_year_code
            )
            if study_year is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.study_year_not_found"),
                )

            full_code = f"{study_year.code}-{body.code.upper()}"
            if len(full_code) > GRADE_CODE_MAX_LENGTH:
                raise HTTPException(
                    status_code=422,
                    detail=translator.gettext("error.grade_code_too_long").format(
                        max=GRADE_CODE_MAX_LENGTH
                    ),
                )

            if len(body.name) > GRADE_NAME_MAX_LENGTH:
                raise HTTPException(
                    status_code=422,
                    detail=translator.gettext("error.grade_name_too_long").format(
                        max=GRADE_NAME_MAX_LENGTH
                    ),
                )

            existing = await self._grade_service.get_by_code(session, full_code)
            if existing is not None:
                raise HTTPException(
                    status_code=409,
                    detail=translator.gettext("error.grade_code_exists").format(
                        code=full_code
                    ),
                )

            catechist_ids = self._provided_catechist_ids(body)
            found = await self._catechist_service.list_by_ids(session, catechist_ids)
            if len(found) != len(catechist_ids):
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.catechist_not_found"),
                )

            grade = await self._grade_service.create(
                session=session,
                study_year_id=study_year.id,
                code=full_code,
                name=body.name,
                leader_catechist_id=body.leader_catechist_id,
                vice_leader_catechist_id=body.vice_leader_catechist_id,
                secretary_catechist_id=body.secretary_catechist_id,
                treasurer_catechist_id=body.treasurer_catechist_id,
            )
            await session.commit()
            await session.refresh(grade)

        return CreateGradeResponse(id=grade.id, code=grade.code, name=grade.name)

    @staticmethod
    def _provided_catechist_ids(body: CreateGradeRequest) -> list[UUID]:
        ids = {
            body.leader_catechist_id,
            body.vice_leader_catechist_id,
            body.secretary_catechist_id,
            body.treasurer_catechist_id,
        }
        return [catechist_id for catechist_id in ids if catechist_id is not None]
