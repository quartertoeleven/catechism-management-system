"""Registry of available seeders."""

from typing import Final

from infrastructure.persistence.seeding.base import Seeder
from infrastructure.persistence.seeding.seeders import CatechistTitleSeeder

SEEDERS: Final[tuple[Seeder, ...]] = (CatechistTitleSeeder(),)


def enabled_seeders() -> tuple[Seeder, ...]:
    """Return every seeder that is currently enabled."""
    return tuple(seeder for seeder in SEEDERS if seeder.enabled)
