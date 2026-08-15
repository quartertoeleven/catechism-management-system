from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cms_common.catechist.models.catechist_schema import CatechistSchema
from cms_db_models.directory.catechist import Catechist


class CatechistService:
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