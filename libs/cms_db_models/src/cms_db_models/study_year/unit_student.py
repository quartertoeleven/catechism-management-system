from typing import TYPE_CHECKING

from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cms_db_models.base import Base

if TYPE_CHECKING:
    from cms_db_models.study_year.unit import Unit
    from cms_db_models.directory.student import Student


class UnitStudent(Base):
    __tablename__ = "unit_students"
    __table_args__ = {"schema": "study_year"}

    unit_id: Mapped[UUID] = mapped_column(
        ForeignKey("study_year.units.id", ondelete="CASCADE"), primary_key=True
    )
    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("directory.students.id", ondelete="CASCADE"), primary_key=True
    )

    unit: Mapped["Unit"] = relationship(
        "Unit", foreign_keys=[unit_id], overlaps="students"
    )
    student: Mapped["Student"] = relationship(
        "Student", foreign_keys=[student_id], overlaps="students"
    )
