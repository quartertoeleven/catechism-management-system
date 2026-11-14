"""Automatic CQRS request handler discovery and wiring."""

from application.cqrs.discovery import (
    HandlerDiscoveryError,
    RequestHandlerRegistration,
    discover_request_handlers,
)
from application.cqrs.mediator import RequestMediatorProvider, bind_requests
from application.cqrs.provider import REQUEST_HANDLERS, ApplicationProvider

__all__ = (
    "REQUEST_HANDLERS",
    "ApplicationProvider",
    "HandlerDiscoveryError",
    "RequestHandlerRegistration",
    "RequestMediatorProvider",
    "bind_requests",
    "discover_request_handlers",
)
