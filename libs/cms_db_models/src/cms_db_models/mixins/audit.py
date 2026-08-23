from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

DEFAULT_AUDIT_USER = "system"


class AuditMixin:
    created: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )
    created_by: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=DEFAULT_AUDIT_USER,
        server_default=DEFAULT_AUDIT_USER,
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
    )
    updated_by: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=DEFAULT_AUDIT_USER,
        server_default=DEFAULT_AUDIT_USER,
    )
