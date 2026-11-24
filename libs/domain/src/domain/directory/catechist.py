"""Catechist domain entity."""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from domain.directory.enums import Gender


@dataclass(frozen=True, slots=True)
class Catechist:
    """Person who teaches catechism."""

    id: uuid.UUID
    code: str
    saint_name: str | None
    first_name: str
    middle_name: str | None
    last_name: str
    gender: Gender
    title_id: uuid.UUID

    @property
    def full_name(self) -> str:
        """Return the display name ordered last, middle, first."""
        parts = (self.last_name, self.middle_name, self.first_name)
        return " ".join(part.strip() for part in parts if part and part.strip())
