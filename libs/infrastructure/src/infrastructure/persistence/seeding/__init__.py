"""Seeding infrastructure for reference data."""

from infrastructure.persistence.seeding.base import Seeder, SeedOutcome
from infrastructure.persistence.seeding.registry import SEEDERS, enabled_seeders
from infrastructure.persistence.seeding.runner import SeedReport, run_seeders
from infrastructure.persistence.seeding.seeders import CatechistTitleSeeder

__all__ = [
    "SEEDERS",
    "CatechistTitleSeeder",
    "SeedOutcome",
    "SeedReport",
    "Seeder",
    "enabled_seeders",
    "run_seeders",
]
