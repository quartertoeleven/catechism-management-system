"""Application dependency injection container."""

from application.cqrs import ApplicationProvider, RequestMediatorProvider
from dishka import AsyncContainer, make_async_container


def create_container() -> AsyncContainer:
    """Build the application dependency injection container."""
    return make_async_container(
        ApplicationProvider(),
        RequestMediatorProvider(),
    )
