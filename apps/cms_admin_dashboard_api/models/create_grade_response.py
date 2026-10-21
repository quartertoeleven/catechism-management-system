from uuid import UUID

from pydantic import BaseModel


class CreateGradeResponse(BaseModel):
    id: UUID
    code: str
    name: str
