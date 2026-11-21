"""Handler for the greeting query."""

from cqrs import RequestHandler

from application.health_check.greeting_query import (
    HELLO_MESSAGE_TEMPLATE,
    GetGreetingQuery,
    GetGreetingResult,
)


class GetGreetingQueryHandler(RequestHandler[GetGreetingQuery, GetGreetingResult]):
    """Build the greeting message for the requested name."""

    async def handle(self, request: GetGreetingQuery) -> GetGreetingResult:
        """Return a greeting addressed to the requested name."""
        return GetGreetingResult(
            message=HELLO_MESSAGE_TEMPLATE.format(name=request.name),
        )
