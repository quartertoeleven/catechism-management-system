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


class Grade(Uuid7PrimaryKeyMixin, StudyYearFk, AuditMixin, Base):
    __tablename__ = "grades"
    __table_args__ = {"schema": "study_year"}

    code: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    leader_catechist_id: Mapped[UUID] = mapped_column(
        ForeignKey("directory.catechists.id", ondelete="RESTRICT"), nullable=False
    )
    vice_leader_catechist_id: Mapped[UUID] = mapped_column(
        ForeignKey("directory.catechists.id", ondelete="RESTRICT"), nullable=False
    )
    secretary_catechist_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("directory.catechists.id", ondelete="RESTRICT"), nullable=True
    )
    treasurer_catechist_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("directory.catechists.id", ondelete="RESTRICT"), nullable=True
    )

    # relationship
    leader_catechist: Mapped["Catechist"] = relationship(
        "Catechist", foreign_keys=[leader_catechist_id]
    )
    vice_leader_catechist: Mapped["Catechist"] = relationship(
        "Catechist", foreign_keys=[vice_leader_catechist_id]
    )
    secretary_catechist: Mapped["Catechist | None"] = relationship(
        "Catechist", foreign_keys=[secretary_catechist_id]
    )
    treasurer_catechist: Mapped["Catechist | None"] = relationship(
        "Catechist", foreign_keys=[treasurer_catechist_id]
    )
