from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UpsertGradeScheduleRequest(BaseModel):
    id: UUID | None = None
    grade_id: UUID
    general_schedule_id: UUID | None = None
    schedule_activity_type_id: int
    name: str
    start_at: datetime
    end_at: datetime | None = None
    detail: str | None = None
    is_attendence_check: bool = True
