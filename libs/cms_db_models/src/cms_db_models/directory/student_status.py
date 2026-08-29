from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from cms_db_models.base import Base
from cms_db_models.mixins import AuditMixin, IsActiveMixin


class StudentStatus(IsActiveMixin, AuditMixin, Base):
    __tablename__ = "student_statuses"
    __table_args__ = {"schema": "directory"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    is_default: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )
