from datetime import datetime
from uuid import UUID

from cms_common.models import CatechistSchema
from pydantic import BaseModel


class GetGradeResponse(BaseModel):
    id: UUID
    study_year_code: str
    code: str
    name: str
    leader_catechist: CatechistSchema | None
    vice_leader_catechist: CatechistSchema | None
    secretary_catechist: CatechistSchema | None
    treasurer_catechist: CatechistSchema | None
    created: datetime
    updated: datetime
