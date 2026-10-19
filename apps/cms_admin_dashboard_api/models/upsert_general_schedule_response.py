from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UpsertGeneralScheduleResponse(BaseModel):
    id: UUID
    study_year_id: UUID
    schedule_activity_type_id: int
    name: str
    start_at: datetime
    end_at: datetime | None
    detail: str | None
    is_attendence_check: bool
    created: datetime
    updated: datetime
