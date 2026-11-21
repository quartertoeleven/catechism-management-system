"""Alembic environment for async SQLAlchemy migrations."""

from __future__ import annotations

import asyncio
from logging.config import fileConfig

from alembic import context
from infrastructure.persistence.metadata import TARGET_METADATA
from infrastructure.persistence.settings import DatabaseSettings
from sqlalchemy import Connection, pool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.schema import CreateSchema

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = DatabaseSettings()

target_metadata = TARGET_METADATA

MANAGED_SCHEMAS = frozenset({"directory", "master_data", "public"})
VERSION_TABLE_SCHEMA = "public"


def include_name(
    name: str | None,
    type_: str,
    parent_names: dict[str, str | None],
) -> bool:
    """Restrict autogenerate reflection to managed schemas."""
    if type_ == "schema":
        return name in MANAGED_SCHEMAS
    return True


def configure_context(**kwargs: object) -> None:
    """Apply settings shared by offline and online migrations."""
    context.configure(
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema=VERSION_TABLE_SCHEMA,
        include_name=include_name,
        compare_type=True,
        compare_server_default=False,
        **kwargs,
    )


def run_migrations_offline() -> None:
    """Run migrations without a live connection."""
    configure_context(
        url=settings.database_url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations against an established connection."""
    configure_context(connection=connection)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create the async engine, ensure schemas, and run migrations."""
    connectable = create_async_engine(
        settings.database_url,
        poolclass=pool.NullPool,
    )

    async with connectable.begin() as connection:
        for schema in sorted(MANAGED_SCHEMAS):
            await connection.execute(CreateSchema(schema, if_not_exists=True))
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations with a live async connection."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
