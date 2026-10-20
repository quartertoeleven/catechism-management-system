from uuid import UUID

from pydantic import BaseModel


class StudyYearListItem(BaseModel):
    id: UUID
    code: str
    name: str
    is_current: bool
    is_readonly: bool


class ListStudyYearsResponse(BaseModel):
    data: list[StudyYearListItem]
