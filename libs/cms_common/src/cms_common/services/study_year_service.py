from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cms_db_models import StudyYear
from cms_common.services.study_year_service_interface import StudyYearServiceInterface


class StudyYearService(StudyYearServiceInterface):
    async def get_by_code(self, session: AsyncSession, code: str) -> StudyYear | None:
        result = await session.execute(select(StudyYear).where(StudyYear.code == code))
        return result.scalar_one_or_none()

    async def get_current_active(self, session: AsyncSession) -> StudyYear | None:
        result = await session.execute(
            select(StudyYear).where(StudyYear.is_current.is_(True))
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        session: AsyncSession,
        code: str,
        name: str,
        is_current: bool,
        is_readonly: bool,
        subject: str | None = None,
        bible_sentence: str | None = None,
        description: str | None = None,
    ) -> StudyYear:
        study_year = StudyYear(
            code=code,
            name=name,
            is_current=is_current,
            is_readonly=is_readonly,
            subject=subject,
            bible_sentence=bible_sentence,
            description=description,
        )
        session.add(study_year)
        return study_year
