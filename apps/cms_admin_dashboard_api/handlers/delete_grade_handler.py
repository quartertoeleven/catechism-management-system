from uuid import UUID

from cms_common.services.grade_service_interface import GradeServiceInterface
from cms_locale import Translator
from fastapi import HTTPException, Response
from handlers.base_handler import BaseAsyncHandler
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DeleteGradeHandler(BaseAsyncHandler):
    def __init__(
        self,
        grade_service: GradeServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._grade_service = grade_service
        self._session_factory = session_factory

    async def handle(self, grade_id: UUID, translator: Translator) -> Response:
        async with self._session_factory() as session:
            grade = await self._grade_service.get_by_id(session, grade_id)
            if grade is None:
                raise HTTPException(
                    status_code=404,
                    detail=translator.gettext("error.grade_not_found"),
                )
            # Units and grade schedules reference the grade with a
            # RESTRICT foreign key — refuse instead of leaking a 500.
            if await self._grade_service.has_dependents(session, grade_id):
                raise HTTPException(
                    status_code=409,
                    detail=translator.gettext("error.grade_in_use"),
                )
            await self._grade_service.delete(session, grade)
            await session.commit()

        return Response(status_code=204)
