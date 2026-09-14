from cms_common.services.schedule_activity_type_service_interface import (
    ScheduleActivityTypeServiceInterface,
)
from handlers.base_handler import BaseAsyncHandler
from models.list_schedule_activity_types_response import (
    ListScheduleActivityTypesResponse,
    ScheduleActivityTypeListItem,
)
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class ListScheduleActivityTypesHandler(BaseAsyncHandler):
    def __init__(
        self,
        schedule_activity_type_service: ScheduleActivityTypeServiceInterface,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._schedule_activity_type_service = schedule_activity_type_service
        self._session_factory = session_factory

    async def handle(self) -> ListScheduleActivityTypesResponse:
        async with self._session_factory() as session:
            activity_types = await self._schedule_activity_type_service.list_all(
                session
            )

        return ListScheduleActivityTypesResponse(
            data=[
                ScheduleActivityTypeListItem(
                    id=at.id,
                    code=at.code,
                    name=at.name,
                    color=at.color,
                    is_system=at.is_system,
                )
                for at in activity_types
            ]
        )
