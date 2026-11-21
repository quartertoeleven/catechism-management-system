"""Database migration commands."""

from collections.abc import Callable
from typing import Annotated

import typer
from alembic.util.exc import CommandError
from infrastructure.persistence import migrations

HEAD_REVISION = "head"

db_app = typer.Typer(
    help="Database migration commands.",
    no_args_is_help=True,
)


def _run(action: Callable[[], None]) -> None:
    """Run an Alembic action and translate command errors into exit codes."""
    try:
        action()
    except CommandError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc


@db_app.command("upgrade")
def upgrade(
    revision: Annotated[str, typer.Argument(help="Target revision.")] = HEAD_REVISION,
) -> None:
    """Apply migrations up to the target revision."""
    _run(lambda: migrations.upgrade(revision))


@db_app.command("downgrade")
def downgrade(
    revision: Annotated[str, typer.Argument(help="Target revision.")],
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Skip confirmation."),
    ] = False,
) -> None:
    """Roll back migrations to the target revision."""
    if not yes:
        typer.confirm(f"Downgrade database to {revision}?", abort=True)
    _run(lambda: migrations.downgrade(revision))


@db_app.command("revision")
def revision(
    message: Annotated[
        str,
        typer.Option("--message", "-m", help="Revision message."),
    ],
    autogenerate: Annotated[
        bool,
        typer.Option("--autogenerate", help="Detect schema changes."),
    ] = False,
) -> None:
    """Create a new migration revision."""
    _run(
        lambda: migrations.revision(
            message,
            autogenerate=autogenerate,
        )
    )


@db_app.command("current")
def current() -> None:
    """Show the current database revision."""
    _run(migrations.current)


@db_app.command("history")
def history() -> None:
    """Show the migration history."""
    _run(migrations.history)


@db_app.command("check")
def check() -> None:
    """Check for model changes not covered by migrations."""
    _run(migrations.check)


@db_app.command("stamp")
def stamp(
    revision: Annotated[str, typer.Argument(help="Revision to stamp.")],
) -> None:
    """Set the database revision without running migrations."""
    _run(lambda: migrations.stamp(revision))
