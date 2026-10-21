from uuid import UUID

from pydantic import BaseModel


class GradeListItem(BaseModel):
    id: UUID
    code: str
    name: str


class ListGradesResponse(BaseModel):
    data: list[GradeListItem]
