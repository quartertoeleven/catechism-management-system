"""CLI entry point."""

import typer

from cli.commands.db import db_app
from cli.commands.seed import seed_app

app = typer.Typer(
    name="cms-cli",
    help="Manage the Catechism Management System.",
    no_args_is_help=True,
)
app.add_typer(db_app, name="db", help="Database migration commands.")
app.add_typer(seed_app, name="seed", help="Seed reference data.")


if __name__ == "__main__":
    app()
