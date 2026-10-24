from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from cms_db_models.study_year import GeneralSchedule, GradeSchedule


class GradeScheduleServiceInterface(ABC):
    @abstractmethod
    async def get_by_id(
        self, session: AsyncSession, schedule_id: UUID
    ) -> GradeSchedule | None: ...

    @abstractmethod
    async def list_by_grade(
        self, session: AsyncSession, grade_id: UUID
    ) -> list[GradeSchedule]: ...

    @abstractmethod
    async def create(
        self,
        session: AsyncSession,
        *,
        study_year_id: UUID,
        grade_id: UUID,
        general_schedule_id: UUID | None,
        schedule_activity_type_id: int,
        name: str,
        start_at: datetime,
        end_at: datetime | None,
        detail: str | None,
        is_attendence_check: bool,
    ) -> GradeSchedule: ...

    @abstractmethod
    async def update(
        self,
        session: AsyncSession,
        schedule: GradeSchedule,
        *,
        general_schedule_id: UUID | None,
        schedule_activity_type_id: int,
        name: str,
        start_at: datetime,
        end_at: datetime | None,
        detail: str | None,
        is_attendence_check: bool,
    ) -> GradeSchedule: ...

    @abstractmethod
    async def delete(self, session: AsyncSession, schedule: GradeSchedule) -> None: ...

    @abstractmethod
    async def list_linked_by_general_ids(
        self, session: AsyncSession, grade_id: UUID, general_ids: list[UUID]
    ) -> dict[UUID, GradeSchedule]: ...

    @abstractmethod
    def apply_sync(
        self,
        schedule: GradeSchedule,
        source: GeneralSchedule,
        *,
        sync_date: bool,
        sync_name: bool,
        sync_start_time: bool,
        sync_end_time: bool,
    ) -> GradeSchedule: ...
