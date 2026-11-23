"""Execute the registered seeders against the database."""

from dataclasses import dataclass

from infrastructure.persistence.engine import build_engine, build_session_factory
from infrastructure.persistence.seeding.registry import enabled_seeders
from infrastructure.persistence.settings import DatabaseSettings


@dataclass(frozen=True, slots=True)
class SeedReport:
    """Outcome of a single seeder run."""

    name: str
    inserted: int
    updated: int


async def run_seeders() -> list[SeedReport]:
    """Run every enabled seeder inside one transaction."""
    settings = DatabaseSettings()
    engine = build_engine(settings)
    session_factory = build_session_factory(engine)
    reports: list[SeedReport] = []
    try:
        async with session_factory.begin() as session:
            for seeder in enabled_seeders():
                outcome = await seeder.run(session)
                reports.append(
                    SeedReport(
                        name=seeder.name,
                        inserted=outcome.inserted,
                        updated=outcome.updated,
                    )
                )
    finally:
        await engine.dispose()
    return reports
