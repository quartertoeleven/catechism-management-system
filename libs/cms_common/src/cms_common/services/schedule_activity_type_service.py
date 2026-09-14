from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cms_db_models.study_year import ScheduleActivityType
from cms_common.services.schedule_activity_type_service_interface import (
    ScheduleActivityTypeServiceInterface,
)


class ScheduleActivityTypeService(ScheduleActivityTypeServiceInterface):
    async def list_all(
        self, session: AsyncSession
    ) -> list[ScheduleActivityType]:
        result = await session.execute(
            select(ScheduleActivityType).order_by(ScheduleActivityType.id)
        )
        return list(result.scalars().all())
