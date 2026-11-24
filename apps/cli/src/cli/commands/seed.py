"""Reference data seeding commands."""

import asyncio

import typer
from infrastructure.persistence.seeding import SEEDERS, SeedReport, run_seeders

seed_app = typer.Typer(
    help="Seed reference data.",
    no_args_is_help=True,
)

ENABLED_STATE = "enabled"
DISABLED_STATE = "disabled"


def _echo_reports(reports: list[SeedReport]) -> None:
    """Print one line per seeded entry."""
    for report in reports:
        typer.echo(
            f"Seeded {report.name}: "
            f"{report.inserted} inserted, {report.updated} updated."
        )


@seed_app.command("run")
def run() -> None:
    """Run every enabled seeder."""
    reports = asyncio.run(run_seeders())
    if not reports:
        typer.echo("No seeders are enabled.")
        return
    _echo_reports(reports)


@seed_app.command("list")
def list_seeders() -> None:
    """List registered seeders and their state."""
    if not SEEDERS:
        typer.echo("No seeders are registered.")
        return
    for seeder in SEEDERS:
        state = ENABLED_STATE if seeder.enabled else DISABLED_STATE
        typer.echo(f"{seeder.name} ({state})")
