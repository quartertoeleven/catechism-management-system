from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

DEFAULT_AUDIT_USER = "system"


class AuditMixin:
    created: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        sort_order=100,
    )
    created_by: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=DEFAULT_AUDIT_USER,
        server_default=DEFAULT_AUDIT_USER,
        sort_order=101,
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        sort_order=102,
    )
    updated_by: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=DEFAULT_AUDIT_USER,
        server_default=DEFAULT_AUDIT_USER,
        sort_order=103,
    )
