from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from cms_db_models.study_year import GeneralSchedule
from cms_common.services.general_schedule_service_interface import (
    GeneralScheduleServiceInterface,
)


class GeneralScheduleService(GeneralScheduleServiceInterface):
    async def get_by_id(
        self, session: AsyncSession, schedule_id: UUID
    ) -> GeneralSchedule | None:
        result = await session.execute(
            select(GeneralSchedule).where(GeneralSchedule.id == schedule_id)
        )
        return result.scalar_one_or_none()

    async def list_by_study_year(
        self, session: AsyncSession, study_year_id: UUID
    ) -> list[GeneralSchedule]:
        result = await session.execute(
            select(GeneralSchedule)
            .options(selectinload(GeneralSchedule.schedule_activity_type))
            .where(GeneralSchedule.study_year_id == study_year_id)
            .order_by(GeneralSchedule.start_at)
        )
        return list(result.scalars().all())

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
    ) -> GeneralSchedule:
        schedule = GeneralSchedule(
            study_year_id=study_year_id,
            schedule_activity_type_id=schedule_activity_type_id,
            name=name,
            start_at=start_at,
            end_at=end_at,
            detail=detail,
            is_attendence_check=is_attendence_check,
        )
        session.add(schedule)
        return schedule

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
    ) -> GeneralSchedule:
        schedule.schedule_activity_type_id = schedule_activity_type_id
        schedule.name = name
        schedule.start_at = start_at
        schedule.end_at = end_at
        schedule.detail = detail
        schedule.is_attendence_check = is_attendence_check
        return schedule

    async def delete(self, session: AsyncSession, schedule: GeneralSchedule) -> None:
        await session.delete(schedule)
