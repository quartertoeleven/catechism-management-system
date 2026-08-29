from datetime import datetime
from typing import TYPE_CHECKING

from uuid import UUID

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cms_db_models.base import Base
from cms_db_models.mixins import (
    AuditMixin,
    StudyYearFk,
    Uuid7PrimaryKeyMixin,
)

if TYPE_CHECKING:
    from cms_db_models.study_year.grade import Grade
    from cms_db_models.study_year.general_schedule import GeneralSchedule
    from cms_db_models.study_year.schedule_activity_type import ScheduleActivityType


class GradeSchedule(Uuid7PrimaryKeyMixin, StudyYearFk, AuditMixin, Base):
    __tablename__ = "grade_schedules"
    __table_args__ = {"schema": "study_year"}

    grade_id: Mapped[UUID] = mapped_column(
        ForeignKey("study_year.grades.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    general_schedule_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("study_year.general_schedules.id", ondelete="SET NULL"),
        nullable=True,
    )
    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    schedule_activity_type_id: Mapped[int] = mapped_column(
        ForeignKey("study_year.schedule_activity_types.id", ondelete="RESTRICT"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    detail: Mapped[str | None] = mapped_column(Text)
    is_attendence_check: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    source_snapshot_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # relationship
    grade: Mapped["Grade"] = relationship("Grade", foreign_keys=[grade_id])
    general_schedule: Mapped["GeneralSchedule | None"] = relationship(
        "GeneralSchedule", foreign_keys=[general_schedule_id]
    )
    schedule_activity_type: Mapped["ScheduleActivityType"] = relationship(
        "ScheduleActivityType", foreign_keys=[schedule_activity_type_id]
    )
