from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from cms_db_models.base import Base


class Catechist(Base):
    __tablename__ = "catechists"
    __table_args__ = {"schema": "people"}

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    saint_name: Mapped[str | None] = mapped_column(String(30))
    first_name: Mapped[str] = mapped_column(String(10), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(25))
    last_name: Mapped[str] = mapped_column(String(10), nullable=False)
