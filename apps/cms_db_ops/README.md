# Commands

All commands are run from workspace root

For auto generating new migration file

`uv run --env-file ../../infrastructure/local/.env --directory apps/cms_db_ops alembic revision --autogenerate -m "<comment-for-the-file>"`

For applying to the latest migration

`uv run --env-file ../../infrastructure/local/.env --directory apps/cms_db_ops alembic upgrade head`

For running all seeders (single transaction, one DB connection)

`uv run --env-file ../../infrastructure/local/.env --directory apps/cms_db_ops python -m db_seeds`

For listing registered seeders

`uv run --env-file ../../infrastructure/local/.env --directory apps/cms_db_ops python -m db_seeds --list`
