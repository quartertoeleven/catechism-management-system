"""Health check controller."""

from application.health_check.greeting_query import DEFAULT_NAME, GetGreetingQuery
from application.health_check.health_check_query import (
    GetHealthQuery,
    HealthStatus,
)
from cqrs import RequestMediator
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response body."""

    status: HealthStatus


class GreetingResponse(BaseModel):
    """Greeting response body."""

    message: str


@router.get("/health", response_model=HealthResponse)
@inject
async def health_check(
    mediator: FromDishka[RequestMediator],
) -> HealthResponse:
    """Return the health status of the application."""
    result = await mediator.send(GetHealthQuery())
    return HealthResponse(status=result.status)


@router.get("/health/hello", response_model=GreetingResponse)
@inject
async def hello(
    mediator: FromDishka[RequestMediator],
    name: str = DEFAULT_NAME,
) -> GreetingResponse:
    """Return a greeting addressed to the requested name."""
    result = await mediator.send(GetGreetingQuery(name=name))
    return GreetingResponse(message=result.message)
