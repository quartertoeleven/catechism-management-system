from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from cms_db_models import StudyYear


class StudyYearServiceInterface(ABC):
    @abstractmethod
    async def get_by_code(
        self, session: AsyncSession, code: str
    ) -> StudyYear | None: ...

    @abstractmethod
    async def get_current_active(self, session: AsyncSession) -> StudyYear | None: ...

    @abstractmethod
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
    ) -> StudyYear: ...
