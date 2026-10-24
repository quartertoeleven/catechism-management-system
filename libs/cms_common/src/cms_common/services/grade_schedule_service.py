from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from cms_db_models.study_year import GeneralSchedule, GradeSchedule
from cms_common.services.grade_schedule_service_interface import (
    GradeScheduleServiceInterface,
)


def _utc_now() -> datetime:
    """Naive UTC now — DB columns are timezone-naive `DateTime`."""
    return datetime.now(UTC).replace(tzinfo=None)


class GradeScheduleService(GradeScheduleServiceInterface):
    async def get_by_id(
        self, session: AsyncSession, schedule_id: UUID
    ) -> GradeSchedule | None:
        result = await session.execute(
            select(GradeSchedule).where(GradeSchedule.id == schedule_id)
        )
        return result.scalar_one_or_none()

    async def list_by_grade(
        self, session: AsyncSession, grade_id: UUID
    ) -> list[GradeSchedule]:
        result = await session.execute(
            select(GradeSchedule)
            .options(selectinload(GradeSchedule.schedule_activity_type))
            .where(GradeSchedule.grade_id == grade_id)
            .order_by(GradeSchedule.start_at)
        )
        return list(result.scalars().all())

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
    ) -> GradeSchedule:
        schedule = GradeSchedule(
            study_year_id=study_year_id,
            grade_id=grade_id,
            general_schedule_id=general_schedule_id,
            schedule_activity_type_id=schedule_activity_type_id,
            name=name,
            start_at=start_at,
            end_at=end_at,
            detail=detail,
            is_attendence_check=is_attendence_check,
            source_snapshot_at=_utc_now() if general_schedule_id else None,
        )
        session.add(schedule)
        return schedule

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
    ) -> GradeSchedule:
        if general_schedule_id != schedule.general_schedule_id:
            # Link changed: restamp (or clear when unlinked).
            schedule.source_snapshot_at = _utc_now() if general_schedule_id else None
        schedule.general_schedule_id = general_schedule_id
        schedule.schedule_activity_type_id = schedule_activity_type_id
        schedule.name = name
        schedule.start_at = start_at
        schedule.end_at = end_at
        schedule.detail = detail
        schedule.is_attendence_check = is_attendence_check
        return schedule

    async def delete(self, session: AsyncSession, schedule: GradeSchedule) -> None:
        await session.delete(schedule)

    async def list_linked_by_general_ids(
        self, session: AsyncSession, grade_id: UUID, general_ids: list[UUID]
    ) -> dict[UUID, GradeSchedule]:
        if not general_ids:
            return {}
        result = await session.execute(
            select(GradeSchedule).where(
                GradeSchedule.grade_id == grade_id,
                GradeSchedule.general_schedule_id.in_(general_ids),
            )
        )
        schedules = list(result.scalars().all())
        return {
            schedule.general_schedule_id: schedule
            for schedule in schedules
            if schedule.general_schedule_id is not None
        }

    def apply_sync(
        self,
        schedule: GradeSchedule,
        source: GeneralSchedule,
        *,
        sync_date: bool,
        sync_name: bool,
        sync_start_time: bool,
        sync_end_time: bool,
    ) -> GradeSchedule:
        """Overwrite checked fields from the general schedule source.

        `date` + `start_time` compose `start_at`; `end_time` maps to `end_at`.
        `detail` is concatenated (source appended to existing text),
        `is_attendence_check` is never touched, and the snapshot is restamped
        because sync refreshes the snapshot.
        """
        if sync_date:
            new_date = source.start_at.date()
            start_at = schedule.start_at.replace(
                year=new_date.year, month=new_date.month, day=new_date.day
            )
            schedule.start_at = start_at
        if sync_start_time:
            schedule.start_at = schedule.start_at.replace(
                hour=source.start_at.hour,
                minute=source.start_at.minute,
                second=source.start_at.second,
                microsecond=source.start_at.microsecond,
            )
        if sync_end_time:
            schedule.end_at = source.end_at
        if sync_name:
            schedule.name = source.name

        if source.detail:
            if not schedule.detail:
                schedule.detail = source.detail
            elif source.detail not in schedule.detail:
                schedule.detail = f"{schedule.detail}\n\n{source.detail}"

        schedule.source_snapshot_at = _utc_now()
        return schedule
