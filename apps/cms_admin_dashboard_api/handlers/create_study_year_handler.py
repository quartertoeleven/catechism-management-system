from cms_common.services.study_year_service_interface import StudyYearServiceInterface
from fastapi import HTTPException, Request
from handlers.base_handler import BaseAsyncHandler
from models.create_study_year_request import CreateStudyYearRequest
from models.create_study_year_response import CreateStudyYearResponse
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class CreateStudyYearHandler(BaseAsyncHandler):
    def __init__(
        self,
        study_year_service: StudyYearServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._study_year_service = study_year_service
        self._session_factory = session_factory

    async def handle(self, request: Request) -> CreateStudyYearResponse:
        body = CreateStudyYearRequest.model_validate(await request.json())

        async with self._session_factory() as session:
            existing = await self._study_year_service.get_by_code(session, body.code)
            if existing is not None:
                raise HTTPException(
                    status_code=409,
                    detail=f"Study year with code '{body.code}' already exists",
                )

            if body.is_current:
                current = await self._study_year_service.get_current_active(session)
                if current is not None:
                    raise HTTPException(
                        status_code=409,
                        detail="A study year is already marked as current",
                    )

            study_year = await self._study_year_service.create(
                session=session,
                code=body.code,
                name=body.name,
                is_current=body.is_current,
                is_readonly=body.is_readonly,
                subject=body.subject,
                bible_sentence=body.bible_sentence,
                description=body.description,
            )
            await session.commit()
            await session.refresh(study_year)

        return CreateStudyYearResponse(
            id=study_year.id,
            code=study_year.code,
            name=study_year.name,
            subject=study_year.subject,
            bible_sentence=study_year.bible_sentence,
            description=study_year.description,
            is_current=study_year.is_current,
            is_readonly=study_year.is_readonly,
            created=study_year.created,
            updated=study_year.updated,
        )
