from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from cms_db_models.study_year import GeneralSchedule


class GeneralScheduleServiceInterface(ABC):
    @abstractmethod
    async def get_by_id(
        self, session: AsyncSession, schedule_id: UUID
    ) -> GeneralSchedule | None: ...

    @abstractmethod
    async def list_by_study_year(
        self, session: AsyncSession, study_year_id: UUID
    ) -> list[GeneralSchedule]: ...

    @abstractmethod
    async def create(
        self,
        session: AsyncSession,
        *,
        study_year_id: UUID,
        schedule_activity_type_id: int,
        name: str,
        start_at: datetime,
        end_at: datetime | None,
        detail: str | None,
        is_attendence_check: bool,
    ) -> GeneralSchedule: ...

    @abstractmethod
    async def update(
        self,
        session: AsyncSession,
        schedule: GeneralSchedule,
        *,
        schedule_activity_type_id: int,
        name: str,
        start_at: datetime,
        end_at: datetime | None,
        detail: str | None,
        is_attendence_check: bool,
    ) -> GeneralSchedule: ...
