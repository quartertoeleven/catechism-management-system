"""Health check query and its result."""

from typing import Final, Literal

from cqrs import Request, Response

HealthStatus = Literal["ok"]

HEALTH_STATUS_OK: Final[HealthStatus] = "ok"


class GetHealthResult(Response):
    """Result of a successful health check."""

    status: HealthStatus = HEALTH_STATUS_OK


class GetHealthQuery(Request[GetHealthResult]):
    """Query asking whether the application is healthy."""
