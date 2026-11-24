"""ORM model for catechists."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, ClassVar

from domain.directory.enums import Gender
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.persistence.base import Base
from infrastructure.persistence.constants import (
    CODE_MAX_LENGTH,
    DIRECTORY_SCHEMA,
    GENDER_ENUM_NAME,
    MASTER_DATA_SCHEMA,
    NAME_MAX_LENGTH,
)
from infrastructure.persistence.mixins import AuditMixin, Uuid7PrimaryKeyMixin

if TYPE_CHECKING:
    from infrastructure.persistence.master_data.catechist_title import (
        CatechistTitle,
    )


class Catechist(Uuid7PrimaryKeyMixin, AuditMixin, Base):
    """Person who teaches catechism."""

    __tablename__ = "catechists"
    __table_args__: ClassVar[dict[str, str]] = {"schema": DIRECTORY_SCHEMA}

    code: Mapped[str] = mapped_column(
        String(CODE_MAX_LENGTH), nullable=False, unique=True
    )
    title_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            f"{MASTER_DATA_SCHEMA}.catechist_titles.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    saint_name: Mapped[str | None] = mapped_column(String(NAME_MAX_LENGTH))
    first_name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(NAME_MAX_LENGTH))
    last_name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    gender: Mapped[Gender] = mapped_column(
        Enum(Gender, name=GENDER_ENUM_NAME, schema=DIRECTORY_SCHEMA),
        nullable=False,
    )

    title: Mapped[CatechistTitle] = relationship(back_populates="catechists")

    # TODO: add once `Unit` and `study_year.unit_catechists` exist:
    # units: Mapped[list[Unit]] = relationship(
    #     secondary="study_year.unit_catechists",
    #     back_populates="catechists",
    # )
