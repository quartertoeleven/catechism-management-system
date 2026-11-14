"""Greeting query and its result."""

from typing import Final

from cqrs import Request, Response

DEFAULT_NAME: Final[str] = "World"
HELLO_MESSAGE_TEMPLATE: Final[str] = "Hello, {name}"


class GetGreetingResult(Response):
    """Result of a greeting."""

    message: str


class GetGreetingQuery(Request[GetGreetingResult]):
    """Query asking for a greeting addressed to a name."""

    name: str = DEFAULT_NAME
