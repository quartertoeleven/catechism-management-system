from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from cms_db_models.study_year import ScheduleActivityType


class ScheduleActivityTypeServiceInterface(ABC):
    @abstractmethod
    async def get_by_id(
        self, session: AsyncSession, type_id: int
    ) -> ScheduleActivityType | None: ...

    @abstractmethod
    async def list_all(self, session: AsyncSession) -> list[ScheduleActivityType]: ...
