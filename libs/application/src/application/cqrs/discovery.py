"""Automatic discovery of CQRS request handlers."""

import importlib
import inspect
import pkgutil
import typing
from collections.abc import Iterator
from dataclasses import dataclass
from types import ModuleType
from typing import Final

from cqrs import IRequest, RequestHandler

DEFAULT_PACKAGE_NAME: Final[str] = "application"
SKIPPED_PACKAGE_PREFIXES: Final[tuple[str, ...]] = ("application.cqrs",)

NOT_A_PACKAGE_MESSAGE: Final[str] = "{package_name!r} is not an importable package."
UNRESOLVED_HANDLER_MESSAGE: Final[str] = (
    "Cannot resolve the request type of handler {handler_name!r}. "
    "It must inherit RequestHandler[RequestType, ResultType] directly."
)
INVALID_REQUEST_MESSAGE: Final[str] = (
    "Handler {handler_name!r} resolves request type {request_name!r}, "
    "which is not a cqrs request."
)
DUPLICATE_HANDLER_MESSAGE: Final[str] = (
    "Request {request_name!r} has multiple handlers: {first_name!r} and "
    "{second_name!r}."
)


class HandlerDiscoveryError(RuntimeError):
    """Raised when request handler discovery finds an invalid registration."""


@dataclass(frozen=True, slots=True)
class RequestHandlerRegistration:
    """One request type paired with the handler that answers it."""

    request_type: type[IRequest]
    handler_type: type[RequestHandler]


def _qualified_name(class_type: type) -> str:
    return f"{class_type.__module__}.{class_type.__qualname__}"


def _iter_package_modules(package_name: str) -> Iterator[ModuleType]:
    package = importlib.import_module(package_name)
    if not hasattr(package, "__path__"):
        raise HandlerDiscoveryError(
            NOT_A_PACKAGE_MESSAGE.format(package_name=package_name),
        )

    yield package

    for module_info in pkgutil.walk_packages(
        package.__path__,
        prefix=f"{package.__name__}.",
    ):
        if module_info.name.startswith(SKIPPED_PACKAGE_PREFIXES):
            continue
        yield importlib.import_module(module_info.name)


def _is_request_handler(class_type: type) -> bool:
    return (
        issubclass(class_type, RequestHandler)
        and not inspect.isabstract(class_type)
        and class_type is not RequestHandler
    )


def _request_type_of(handler_type: type[RequestHandler]) -> type[IRequest]:
    bases = (*getattr(handler_type, "__orig_bases__", ()), *handler_type.__bases__)
    for base in bases:
        if typing.get_origin(base) is not RequestHandler:
            continue

        arguments = typing.get_args(base)
        if not arguments:
            continue

        request_type = arguments[0]
        if not isinstance(request_type, type):
            continue

        return request_type

    raise HandlerDiscoveryError(
        UNRESOLVED_HANDLER_MESSAGE.format(
            handler_name=_qualified_name(handler_type),
        ),
    )


def _iter_handler_classes(module: ModuleType) -> Iterator[type[RequestHandler]]:
    for _, candidate in inspect.getmembers(module, inspect.isclass):
        if candidate.__module__ != module.__name__:
            continue
        if not _is_request_handler(candidate):
            continue
        yield candidate


def discover_request_handlers(
    package_name: str = DEFAULT_PACKAGE_NAME,
) -> tuple[RequestHandlerRegistration, ...]:
    """Find every request handler declared in the application package."""
    registrations: dict[type[IRequest], type[RequestHandler]] = {}

    for module in _iter_package_modules(package_name):
        for handler_type in _iter_handler_classes(module):
            request_type = _request_type_of(handler_type)
            if not issubclass(request_type, IRequest):
                raise HandlerDiscoveryError(
                    INVALID_REQUEST_MESSAGE.format(
                        handler_name=_qualified_name(handler_type),
                        request_name=_qualified_name(request_type),
                    ),
                )

            existing_handler = registrations.get(request_type)
            if existing_handler is not None:
                raise HandlerDiscoveryError(
                    DUPLICATE_HANDLER_MESSAGE.format(
                        request_name=_qualified_name(request_type),
                        first_name=_qualified_name(existing_handler),
                        second_name=_qualified_name(handler_type),
                    ),
                )

            registrations[request_type] = handler_type

    ordered = sorted(
        registrations.items(),
        key=lambda item: (item[0].__module__, item[0].__qualname__),
    )
    return tuple(
        RequestHandlerRegistration(
            request_type=request_type,
            handler_type=handler_type,
        )
        for request_type, handler_type in ordered
    )
