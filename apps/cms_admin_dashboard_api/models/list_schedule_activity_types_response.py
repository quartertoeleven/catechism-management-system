from pydantic import BaseModel


class ScheduleActivityTypeListItem(BaseModel):
    id: int
    code: str
    name: str
    color: str | None
    is_system: bool


class ListScheduleActivityTypesResponse(BaseModel):
    data: list[ScheduleActivityTypeListItem]
