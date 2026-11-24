"""ORM model for catechist titles."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.persistence.base import Base
from infrastructure.persistence.constants import (
    CODE_MAX_LENGTH,
    MASTER_DATA_SCHEMA,
    NAME_MAX_LENGTH,
)
from infrastructure.persistence.mixins import AuditMixin, Uuid7PrimaryKeyMixin

if TYPE_CHECKING:
    from infrastructure.persistence.directory.catechist import Catechist


class CatechistTitle(Uuid7PrimaryKeyMixin, AuditMixin, Base):
    """Classification assigned to a catechist."""

    __tablename__ = "catechist_titles"
    __table_args__: ClassVar[dict[str, str]] = {"schema": MASTER_DATA_SCHEMA}

    code: Mapped[str] = mapped_column(
        String(CODE_MAX_LENGTH), nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)

    catechists: Mapped[list[Catechist]] = relationship(back_populates="title")
