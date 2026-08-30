# Catechism Management System (CMS)

A monorepo for managing catechism teaching activities. *Project is currently under-development*

_Note: The Catechism Management System (CMS) is being developed primarily for Tam Ha Parish. The system is created to contribute to managing catechism students in the parish more effectively and modernly._


## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.14 |
| REST API | FastAPI, dependency-injector |
| Database | PostgreSQL 18 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic 1.18 |
| Driver | psycopg 3 |
| Frontend | Vue 3, Nuxt 4, NuxtUI 4 |
| Package mgmt | uv (workspace) |
| Lint / Format | ruff |
| Infrastructure | Docker Compose |

## Getting Started

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- Docker & Docker Compose

### Setup

```bash
# Start PostgreSQL
docker compose -f infrastructure/local/docker-compose.yaml up -d

# Install libraries and dependencies
uv sync

# Run database migrations
uv run --env-file infrastructure/local/.env \
  --directory apps/cms_db_ops alembic upgrade head

# Start the API server (hot-reload)
uv run --directory apps/cms_admin_dashboard_api \
  uvicorn cms_admin_dashboard_api.main:create_app --factory --reload
```
