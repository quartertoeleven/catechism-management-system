# Project Overview

The Catechism Management System (CMS) is a system designed to help manage catechism teaching activities.

# Architecture

The project is laid out as a monorepo - managed using `uv` and follows the Domain-Driven Design (DDD) approach and Clean Architecture architect.

# Structure

- `apps` directory contains the presentation layer (Frontend, RestAPI)
- `libs` contains the application, infrastructure and domain layer.

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
    - SQLAlchemy 2.x as the ORM
    - Alembic 1.18 are utilized for database operation (migration creation, upgrade, downgrade,…).
- **Others**:
    - `uv` for packages and project management.
    - `ruff` as the Python linter and code formatter.
    - `pnpm` as the package manager for the frontend project

# Build & Commands

- Never invoke bare Python or pip: Always use `uv run <command>` or `uvx <package>` to execute scripts.

# Code Style Guidelines

## For Python

- Use **PEP 8** as the style guide for Python code (utilize `ruff` whenever possible).
- Only consider the dependency injection pattern whenever make sense
- Do not hard-code strings / values; extract them to constants.
- Always use type hints.

## For frontend
(will update later)

# Boundaries
- **YOU MUST NOT** remove, delete, or destroy anything. Whenever there is a need to remove something, give the user the list of the files / directories, and they will do it manually.
- **YOU MUST NOT** install any new packages / libraries automatically. Whenever there is a need to installing new libraries / packages, tell the user to do that manually.
- **YOU MUST NOT** stage or commit anything automatically. The user will always do that manually. If the user specifically asks for that, refuse them immediately.
- **DO NOT ASSUME**. If anything is unclear, make those into open questions/risks and ask the user for more details.
- **ALWAYS WARN AND PROMPT DEVELOPERS** if they suggest something that breaks DDD and Clean Architecture
- **ALWAYS FORMAT THE PYTHON SCRIPT** with `ruff` after modifying the code.