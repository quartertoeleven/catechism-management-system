from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class SyncGradeScheduleRequest(BaseModel):
    grade_id: UUID
    date_from: date | None = None
    date_to: date | None = None
    schedule_activity_type_ids: list[int] = Field(min_length=1)
    sync_date: bool = True
    sync_name: bool = True
    sync_start_time: bool = True
    sync_end_time: bool = True
