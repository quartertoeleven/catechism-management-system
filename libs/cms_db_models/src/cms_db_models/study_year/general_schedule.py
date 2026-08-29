from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cms_db_models.base import Base
from cms_db_models.mixins import (
    AuditMixin,
    StudyYearFk,
    Uuid7PrimaryKeyMixin,
)
from cms_db_models.study_year.schedule_activity_type import ScheduleActivityType


class GeneralSchedule(Uuid7PrimaryKeyMixin, StudyYearFk, AuditMixin, Base):
    __tablename__ = "general_schedules"
    __table_args__ = {"schema": "study_year"}

    start_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    schedule_activity_type_id: Mapped[int] = mapped_column(
        ForeignKey("study_year.schedule_activity_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    detail: Mapped[str | None] = mapped_column(Text)
    is_attendence_check: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )

    # relationship
    schedule_activity_type: Mapped["ScheduleActivityType"] = relationship(
        "ScheduleActivityType"
    )
