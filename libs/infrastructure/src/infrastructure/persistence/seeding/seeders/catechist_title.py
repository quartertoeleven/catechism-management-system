"""Seed data for catechist titles."""

import uuid
from dataclasses import dataclass
from typing import Final

from sqlalchemy import func, literal_column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.persistence.master_data.catechist_title import CatechistTitle
from infrastructure.persistence.seeding.base import Seeder, SeedOutcome
from infrastructure.persistence.seeding.constants import SEED_ACTOR

CONFLICT_COLUMNS: Final[tuple[str, ...]] = ("code",)
INSERTED_FLAG_SQL: Final[str] = "xmax = 0"
INSERTED_FLAG_LABEL: Final[str] = "inserted"


@dataclass(frozen=True, slots=True)
class CatechistTitleSeed:
    """A single catechist title row to seed."""

    id: uuid.UUID
    code: str
    name: str


CATECHIST_TITLE_SEEDS: Final[tuple[CatechistTitleSeed, ...]] = (
    CatechistTitleSeed(uuid.UUID("01a207d7-491a-7063-82fc-019478e8ecf7"), "CHA", "Cha"),
    CatechistTitleSeed(
        uuid.UUID("01a207d7-491a-7063-82fc-0195b86ae4e7"), "THAY", "Thầy"
    ),
    CatechistTitleSeed(uuid.UUID("01a207d7-491a-7063-82fc-0196f17f7a89"), "SO", "Sơ"),
    CatechistTitleSeed(uuid.UUID("01a207d7-491a-7063-82fc-0197f0fb928b"), "ANH", "Anh"),
    CatechistTitleSeed(uuid.UUID("01a207d7-491a-7063-82fc-01986cf648b3"), "CHI", "Chị"),
)


class CatechistTitleSeeder(Seeder):
    """Upsert the catechist titles."""

    name = "catechist_titles"
    enabled = True

    async def run(self, session: AsyncSession) -> SeedOutcome:
        """Insert missing titles and refresh the names of existing ones."""
        statement = insert(CatechistTitle).values(
            [
                {
                    "id": seed.id,
                    "code": seed.code,
                    "name": seed.name,
                    "created_by": SEED_ACTOR,
                    "updated_by": SEED_ACTOR,
                }
                for seed in CATECHIST_TITLE_SEEDS
            ]
        )
        statement = statement.on_conflict_do_update(
            index_elements=CONFLICT_COLUMNS,
            set_={
                "name": statement.excluded.name,
                "updated_by": SEED_ACTOR,
                "updated_at": func.now(),
            },
        ).returning(
            # PostgreSQL leaves `xmax` at 0 for rows that were inserted.
            literal_column(INSERTED_FLAG_SQL).label(INSERTED_FLAG_LABEL)
        )

        result = await session.execute(statement)
        inserted = sum(result.scalars().all())
        return SeedOutcome(
            inserted=inserted,
            updated=len(CATECHIST_TITLE_SEEDS) - inserted,
        )
