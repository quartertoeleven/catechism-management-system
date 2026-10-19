from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GeneralScheduleListItem(BaseModel):
    id: UUID
    schedule_activity_type_id: int
    schedule_activity_type_name: str
    schedule_activity_type_color: str | None
    name: str
    start_at: datetime
    end_at: datetime | None
    detail: str | None
    is_attendence_check: bool
    updated: datetime


class ListGeneralSchedulesResponse(BaseModel):
    data: list[GeneralScheduleListItem]
