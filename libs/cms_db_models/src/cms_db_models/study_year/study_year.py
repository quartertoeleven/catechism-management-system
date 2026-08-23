from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from cms_db_models.base import Base
from cms_db_models.mixins import (
    AuditMixin,
    SoftDeleteMixin,
    Uuid7PrimaryKeyMixin,
)


class StudyYear(Uuid7PrimaryKeyMixin, SoftDeleteMixin, AuditMixin, Base):
    __tablename__ = "study_years"
    __table_args__ = {"schema": "study_year"}

    code: Mapped[str] = mapped_column(
        String(15), nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(100))
    bible_sentence: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    is_current: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    is_readonly: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
