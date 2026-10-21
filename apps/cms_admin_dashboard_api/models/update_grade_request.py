from uuid import UUID

from pydantic import BaseModel


class UpdateGradeRequest(BaseModel):
    name: str
    leader_catechist_id: UUID | None = None
    vice_leader_catechist_id: UUID | None = None
    secretary_catechist_id: UUID | None = None
    treasurer_catechist_id: UUID | None = None
