from __future__ import annotations

from typing import TYPE_CHECKING

from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from cms_db_models.study_year import StudyYear


class StudyYearFk:
    study_year_id: Mapped[UUID] = mapped_column(
        ForeignKey("study_year.study_years.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    study_year: Mapped["StudyYear"] = relationship("StudyYear")
