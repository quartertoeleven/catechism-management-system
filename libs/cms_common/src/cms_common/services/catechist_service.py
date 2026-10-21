from uuid import UUID

from cms_db_models.directory.catechist import Catechist
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from cms_common.models.catechist_schema import CatechistSchema


class CatechistService:
    SEARCH_LIMIT = 20

    @staticmethod
    async def search(session: AsyncSession, query: str | None) -> list[Catechist]:
        stmt = select(Catechist)
        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(
                or_(
                    Catechist.code.ilike(pattern),
                    Catechist.saint_name.ilike(pattern),
                    Catechist.first_name.ilike(pattern),
                    Catechist.middle_name.ilike(pattern),
                    Catechist.last_name.ilike(pattern),
                )
            )
        result = await session.execute(
            stmt.order_by(Catechist.code).limit(CatechistService.SEARCH_LIMIT)
        )
        return list(result.scalars().all())

    @staticmethod
    async def list_by_ids(session: AsyncSession, ids: list[UUID]) -> list[Catechist]:
        result = await session.execute(select(Catechist).where(Catechist.id.in_(ids)))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_code(
        session: AsyncSession, code: str | None
    ) -> CatechistSchema | None:
        if not code:
            return None
        query = select(Catechist).where(Catechist.code == code)
        result = await session.execute(query)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return CatechistSchema(
            id=model.id,
            code=model.code,
            title=model.title,
            saint_name=model.saint_name,
            first_name=model.first_name,
            middle_name=model.middle_name,
            last_name=model.last_name,
            gender=model.gender,
        )
