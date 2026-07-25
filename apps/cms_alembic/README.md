# Commands

All commands are run from workspace root

For auto generating new migration file

`uv run --env-file ../../infrastructure/local/.env --directory apps/cms_alembic alembic revision --autogenerate -m "<comment-for-the-file>"`

For applying to the latest migration

`uv run --env-file ../../infrastructure/local/.env --directory apps/cms_alembic alembic upgrade head`
