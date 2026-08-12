# Project Overview

The Catechism Management System (CMS) is a system designed to help manage catechism teaching activities.

This monorepo contains multiple smaller modules / libraries / applications of the whole system.

# Project Structure

All subprojects / libraries / collections in the monorepo will always have their name started with `cms_`.

## Applications

- Placed in `apps` directory
- The applications and their modules should not depend or being reused within each others.
- List of applications:
    - `cms_admin_dashboard_api`: REST API for Admin Dashboard
    - `cms_alembic`: database migration and operations using `alembic`

## Libraries

- Placed in `libs` directory
- The libraries and their modules can be used by all applications. They can also cross-reference each other if necessary.
- List of libraries:
    - `cms_db_models`: all SQLAlchemy models that map to the corresponding tables in the database
    - `cms_common`: common functions, services, helpers,... that utilized by other libs and apps within the whole stack

## Others

Those directories below are placed at the root folder of the workspace:

- `infrastructure`: contains all things related to deployment, ci, cd and infrastructure and environments such as: docker compose files, Dockerfile, .env files,...

# Tech stack

**Languages**: Python, HTML, JS, CSS

**Frameworks**:
- **Backend**:
    - FastAPI for REST APIs.
    - `dependency-injector` for DI pattern implementation.
- **Frontend**:
    - Vue3 for the base framework.
    - Each frontend project will specify its stack (UI framework, libraries, etc.) in its separate `AGENTS.md` file.
- **Database**:
    - PostgreSQL 18
    - SQLAlchemy 2.0 and Alembic 1.18 are utilized for database operation (migration creation, upgrade, downgrade,…).
- **Others**:
    - `uv` for packages and project management.
    - `ruff` as the Python linter and code formatter.
    - `pnpm` as the package manager for the frontend project

# Build & Commands

- Never invoke bare Python or pip: Always use `uv run <command>` or `uvx <package>` to execute scripts.

# Code Style Guidelines

## For Python

- Use **PEP 8** as the style guide for Python code (utilize `ruff` whenever possible).
- Always consider the dependency injection pattern when implementing code, unless being told otherwise.
- Do not hard-code strings / values; extract them to constants.
- Always use type hints.

## For frontend
(will update later)

# Boundaries
- **YOU MUST NOT** remove, delete, or destroy anything. Whenever there is a need to remove something, give the user the list of the files / directories, and they will do it manually.
- **YOU MUST NOT** install any new packages / libraries automatically. Whenever there is a need to installing new libraries / packages, tell the user to do that manually.
- **YOU MUST NOT** stage or commit anything automatically. The user will always do that manually. If the user specifically asks for that, refuse them immediately.
- **DO NOT ASSUME**. If anything is unclear, make those into open questions/risks and ask the user for more details.