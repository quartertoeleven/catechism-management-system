# Plan: Centralize Async DB Session via Dependency Injection

## Goal
Stop manually passing the SQLAlchemy async session through every layer (controller → handler → service). Instead, wire the session at the container level so it's injected directly into whichever service needs it, per request.

## Stack
- FastAPI (API layer)
- `dependency-injector` (DI container/wiring)
- SQLAlchemy 2.x async (`AsyncSession`)

## Architectural rule
Each layer only knows about the layer directly beneath it:
- **Controller** (FastAPI route) → depends on **Handler**
- **Handler** → depends on **Service**
- **Service** → depends on **DB session** (and any other resources it needs)

The DB session must never be passed as a function parameter or threaded through the controller/handler. It is only ever consumed inside a service's constructor.

## Steps

1. **Set up the container (`containers.py`)**
   - Define a `providers.Singleton` for the async engine (`create_async_engine`).
   - Define a `providers.Singleton` for the `async_sessionmaker`, bound to the engine.
   - Define a `providers.Resource` (not `Singleton`/`Factory`) for the session itself, so a fresh session is created per resolution and can be cleaned up afterward.
   - Register `WiringConfiguration` pointing at every handler module that needs injection.

2. **Refactor services to accept the session via constructor**
   - Every service that touches the DB (e.g. `DataService`) should take `session: AsyncSession` as an `__init__` parameter — never as a method parameter.
   - Register each such service in the container as a `providers.Factory(ServiceClass, session=db_session)`.
   - This pattern must be repeated for every new DB-touching service going forward: same `db_session` provider, injected at construction time.

3. **Refactor handlers to depend only on services**
   - Handlers use `@inject` + `Provide[Container.xxx_service]` to receive a ready-to-use service instance.
   - Handlers must never reference the session or the container's DB internals directly.

4. **Refactor controllers to depend only on handlers**
   - FastAPI routes use `Depends(HandlerClass)` as usual.
   - No session or service wiring logic belongs in the controller.

5. **Handle session lifecycle/cleanup properly**
   - Since `providers.Resource` is being used, verify sessions are actually closed after each request (not leaked).
   - Investigate whether `container.reset_singletons()` or a FastAPI middleware hook is needed to trigger resource teardown per request — this needs explicit testing, it's the trickiest part of the setup.

6. **Validate**
   - Write a test that fires two concurrent requests and confirms each gets its own isolated session (no cross-request session sharing/leakage).
   - Confirm existing endpoints still function after migrating off manually-passed sessions.

## Non-goals
- This plan does not cover transaction management strategy (e.g. unit-of-work pattern) — that can be layered on top later if needed.
- Does not cover synchronous SQLAlchemy sessions, only the async engine/session path.
