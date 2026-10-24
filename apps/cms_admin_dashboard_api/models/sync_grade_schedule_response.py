from pydantic import BaseModel


class SyncGradeScheduleResponse(BaseModel):
    created: int
    updated: int
