"""Handler for the health check query."""

from cqrs import RequestHandler

from application.health_check.health_check_query import (
    GetHealthQuery,
    GetHealthResult,
)


class GetHealthQueryHandler(RequestHandler[GetHealthQuery, GetHealthResult]):
    """Answer the health check query."""

    async def handle(self, request: GetHealthQuery) -> GetHealthResult:
        """Return the healthy status of the application."""
        return GetHealthResult()
