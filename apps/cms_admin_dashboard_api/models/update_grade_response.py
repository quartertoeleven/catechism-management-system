from uuid import UUID

from pydantic import BaseModel


class UpdateGradeResponse(BaseModel):
    id: UUID
    code: str
    name: str
