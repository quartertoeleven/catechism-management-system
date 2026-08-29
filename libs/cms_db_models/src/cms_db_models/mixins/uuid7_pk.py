from uuid import UUID, uuid7

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class Uuid7PrimaryKeyMixin:
    id: Mapped[UUID] = mapped_column(
        primary_key=True, default=uuid7, server_default=func.uuidv7(), sort_order=-10
    )
