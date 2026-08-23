from uuid import UUID, uuid7

from sqlalchemy import Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from cms_db_models.base import Base
from cms_db_models.enums import CatechistTitle, Gender


class Catechist(Base):
    __tablename__ = "catechists"
    __table_args__ = {"schema": "directory"}

    id: Mapped[UUID] = mapped_column(
        primary_key=True, default=uuid7, server_default=func.uuidv7()
    )
    code: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True
    )  # should be GLV-INITIAL (for example: GLV-NQM)
    title: Mapped[CatechistTitle] = mapped_column(Enum(CatechistTitle), nullable=False)
    saint_name: Mapped[str | None] = mapped_column(String(30))
    first_name: Mapped[str] = mapped_column(String(10), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(25))
    last_name: Mapped[str] = mapped_column(String(10), nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
