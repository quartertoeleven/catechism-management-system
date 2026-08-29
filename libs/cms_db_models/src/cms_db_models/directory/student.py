from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cms_db_models.base import Base
from cms_db_models.enums import Gender
from cms_db_models.mixins import (
    AuditMixin,
    IsActiveMixin,
    Uuid7PrimaryKeyMixin,
)

if TYPE_CHECKING:
    from cms_db_models.directory.student_status import StudentStatus


class Student(Uuid7PrimaryKeyMixin, AuditMixin, IsActiveMixin, Base):
    __tablename__ = "students"
    __table_args__ = {"schema": "directory"}

    code: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )
    saint_name: Mapped[str | None] = mapped_column(String(30))
    first_name: Mapped[str] = mapped_column(String(10), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(25))
    last_name: Mapped[str] = mapped_column(String(10), nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    student_status_id: Mapped[int] = mapped_column(
        ForeignKey("directory.student_statuses.id", ondelete="RESTRICT"),
        nullable=False,
    )
    note: Mapped[str | None] = mapped_column(String(255))

    # relationship
    student_status: Mapped["StudentStatus"] = relationship(
        "StudentStatus", foreign_keys=[student_status_id]
    )
