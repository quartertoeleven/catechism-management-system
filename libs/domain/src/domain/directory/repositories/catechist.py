"""Catechist repository port."""

from __future__ import annotations

import uuid
from typing import Protocol

from domain.directory.catechist import Catechist


class CatechistRepository(Protocol):
    """Read and write catechists."""

    async def get(self, catechist_id: uuid.UUID) -> Catechist | None:
        """Return the catechist with the given id, if any."""
        ...
