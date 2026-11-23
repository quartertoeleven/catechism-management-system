"""Contract shared by every seeder."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True, slots=True)
class SeedOutcome:
    """Per-seeder counts produced by a single run."""

    inserted: int
    updated: int


class Seeder(ABC):
    """An idempotent unit of reference data."""

    name: ClassVar[str]
    enabled: ClassVar[bool] = True

    @abstractmethod
    async def run(self, session: AsyncSession) -> SeedOutcome:
        """Apply this seeder's data and report the resulting counts."""
