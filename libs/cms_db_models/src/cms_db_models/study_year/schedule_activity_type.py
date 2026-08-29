from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from cms_db_models.base import Base
from cms_db_models.mixins import AuditMixin, IsActiveMixin


class ScheduleActivityType(IsActiveMixin, AuditMixin, Base):
    __tablename__ = "schedule_activity_types"
    __table_args__ = {"schema": "study_year"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
