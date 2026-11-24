"""SQLAlchemy implementation of the catechist repository."""

from __future__ import annotations

import uuid

from domain.directory.catechist import Catechist as CatechistEntity
from domain.directory.enums import Gender
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.persistence.directory.catechist import Catechist


class SqlAlchemyCatechistRepository:
    """Read catechists from PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, catechist_id: uuid.UUID) -> CatechistEntity | None:
        """Return the catechist with the given id, if any."""
        row = await self._session.get(Catechist, catechist_id)
        if row is None:
            return None
        return _to_entity(row)


def _to_entity(row: Catechist) -> CatechistEntity:
    return CatechistEntity(
        id=row.id,
        code=row.code,
        saint_name=row.saint_name,
        first_name=row.first_name,
        middle_name=row.middle_name,
        last_name=row.last_name,
        gender=Gender(row.gender),
        title_id=row.title_id,
    )
