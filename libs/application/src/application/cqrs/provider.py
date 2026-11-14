"""Dishka provider for discovered CQRS request handlers."""

from typing import Final

from dishka import Provider, Scope, provide_all

from application.cqrs.discovery import (
    RequestHandlerRegistration,
    discover_request_handlers,
)

REQUEST_HANDLERS: Final[tuple[RequestHandlerRegistration, ...]] = (
    discover_request_handlers()
)


class ApplicationProvider(Provider):
    """Provide every discovered CQRS request handler."""

    handlers = provide_all(
        *(registration.handler_type for registration in REQUEST_HANDLERS),
        scope=Scope.REQUEST,
    )
