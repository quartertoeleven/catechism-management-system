from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateStudyYearResponse(BaseModel):
    id: UUID
    code: str
    name: str
    subject: str | None
    bible_sentence: str | None
    description: str | None
    is_current: bool
    is_readonly: bool
    created: datetime
    updated: datetime
