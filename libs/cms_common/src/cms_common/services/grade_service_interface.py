from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from cms_db_models.study_year import Grade


class GradeServiceInterface(ABC):
    @abstractmethod
    async def list_by_study_year(
        self, session: AsyncSession, study_year_id: UUID
    ) -> list[Grade]: ...

    @abstractmethod
    async def get_by_code(self, session: AsyncSession, code: str) -> Grade | None: ...

    @abstractmethod
    async def get_by_id(
        self, session: AsyncSession, grade_id: UUID
    ) -> Grade | None: ...

    @abstractmethod
    async def update(
        self,
        session: AsyncSession,
        grade: Grade,
        *,
        name: str,
        leader_catechist_id: UUID | None,
        vice_leader_catechist_id: UUID | None,
        secretary_catechist_id: UUID | None,
        treasurer_catechist_id: UUID | None,
    ) -> Grade: ...

    @abstractmethod
    async def has_dependents(self, session: AsyncSession, grade_id: UUID) -> bool: ...

    @abstractmethod
    async def delete(self, session: AsyncSession, grade: Grade) -> None: ...

    @abstractmethod
    async def create(
        self,
        session: AsyncSession,
        *,
        study_year_id: UUID,
        code: str,
        name: str,
        leader_catechist_id: UUID | None,
        vice_leader_catechist_id: UUID | None,
        secretary_catechist_id: UUID | None,
        treasurer_catechist_id: UUID | None,
    ) -> Grade: ...
