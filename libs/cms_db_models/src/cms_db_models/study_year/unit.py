from typing import TYPE_CHECKING

from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cms_db_models.base import Base
from cms_db_models.mixins import (
    AuditMixin,
    StudyYearFk,
    Uuid7PrimaryKeyMixin,
)

if TYPE_CHECKING:
    from cms_db_models.directory.catechist import Catechist
    from cms_db_models.directory.student import Student
    from cms_db_models.study_year.grade import Grade


class Unit(Uuid7PrimaryKeyMixin, StudyYearFk, AuditMixin, Base):
    __tablename__ = "units"
    __table_args__ = {"schema": "study_year"}

    code: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    grade_id: Mapped[UUID] = mapped_column(
        ForeignKey("study_year.grades.id", ondelete="RESTRICT"), nullable=False
    )

    # relationship
    grade: Mapped["Grade"] = relationship("Grade", foreign_keys=[grade_id])
    catechists: Mapped[list["Catechist"]] = relationship(
        "Catechist", secondary="study_year.unit_catechists", back_populates="units"
    )
    students: Mapped[list["Student"]] = relationship(
        "Student", secondary="study_year.unit_students"
    )
