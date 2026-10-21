from uuid import UUID

from pydantic import BaseModel


class CreateGradeRequest(BaseModel):
    study_year_code: str
    code: str
    name: str
    leader_catechist_id: UUID | None = None
    vice_leader_catechist_id: UUID | None = None
    secretary_catechist_id: UUID | None = None
    treasurer_catechist_id: UUID | None = None
