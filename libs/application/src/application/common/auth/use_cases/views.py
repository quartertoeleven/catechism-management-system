"""Transport-neutral views returned by authentication use cases."""

import uuid
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserView:
    """Profile of the authenticated user."""

    subject: str
    name: str | None
    email: str | None
    picture: str | None


@dataclass(frozen=True, slots=True)
class CatechistView:
    """Catechist linked to the authenticated user."""

    id: uuid.UUID
    code: str
    full_name: str
