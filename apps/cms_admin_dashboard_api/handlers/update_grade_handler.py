from uuid import UUID

from cms_common.services.catechist_service import CatechistService
from cms_common.services.grade_service_interface import GradeServiceInterface
from cms_db_models.study_year.grade import GRADE_NAME_MAX_LENGTH
from cms_locale import Translator
from fastapi import HTTPException
from handlers.base_handler import BaseAsyncHandler
from models.update_grade_request import UpdateGradeRequest
from models.update_grade_response import UpdateGradeResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class UpdateGradeHandler(BaseAsyncHandler):
    def __init__(
        self,
        grade_service: GradeServiceInterface,
        catechist_service: CatechistService,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._grade_service = grade_service
        self._catechist_service = catechist_service
        self._session_factory = session_factory

    async def handle(
        self, grade_id: UUID, body: UpdateGradeRequest, translator: Translator
    ) -> UpdateGradeResponse:
        async with self._session_factory() as session:
            grade = await self._grade_service.get_by_id(session, grade_id)
            if grade is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.grade_not_found"),
                )

            if len(body.name) > GRADE_NAME_MAX_LENGTH:
                raise HTTPException(
                    status_code=422,
                    detail=translator.gettext("error.grade_name_too_long").format(
                        max=GRADE_NAME_MAX_LENGTH
                    ),
                )

            catechist_ids = self._provided_catechist_ids(body)
            if catechist_ids:
                found = await self._catechist_service.list_by_ids(
                    session, catechist_ids
                )
                if len(found) != len(catechist_ids):
                    raise HTTPException(
                        status_code=404,
                        detail=translator.gettext("error.catechist_not_found"),
                    )

            # Code is immutable — never reassigned here.
            grade = await self._grade_service.update(
                session,
                grade,
                name=body.name,
                leader_catechist_id=body.leader_catechist_id,
                vice_leader_catechist_id=body.vice_leader_catechist_id,
                secretary_catechist_id=body.secretary_catechist_id,
                treasurer_catechist_id=body.treasurer_catechist_id,
            )
            await session.commit()
            await session.refresh(grade)

        return UpdateGradeResponse(id=grade.id, code=grade.code, name=grade.name)

    @staticmethod
    def _provided_catechist_ids(body: UpdateGradeRequest) -> list[UUID]:
        ids = {
            body.leader_catechist_id,
            body.vice_leader_catechist_id,
            body.secretary_catechist_id,
            body.treasurer_catechist_id,
        }
        return [catechist_id for catechist_id in ids if catechist_id is not None]
