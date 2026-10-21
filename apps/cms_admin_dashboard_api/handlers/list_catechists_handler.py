from uuid import UUID

from cms_common.models import CatechistSchema
from cms_common.services.catechist_service import CatechistService
from handlers.base_handler import BaseAsyncHandler
from models.list_catechists_response import ListCatechistsResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class ListCatechistsHandler(BaseAsyncHandler):
    def __init__(
        self,
        catechist_service: CatechistService,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._catechist_service = catechist_service
        self._session_factory = session_factory

    async def handle(
        self, query: str | None, ids: list[UUID] | None = None
    ) -> ListCatechistsResponse:
        async with self._session_factory() as session:
            if ids:
                catechists = await self._catechist_service.list_by_ids(session, ids)
            else:
                catechists = await self._catechist_service.search(session, query)

        return ListCatechistsResponse(
            data=[
                CatechistSchema(
                    id=catechist.id,
                    code=catechist.code,
                    title=catechist.title,
                    saint_name=catechist.saint_name,
                    first_name=catechist.first_name,
                    middle_name=catechist.middle_name,
                    last_name=catechist.last_name,
                    gender=catechist.gender,
                )
                for catechist in catechists
            ]
        )
