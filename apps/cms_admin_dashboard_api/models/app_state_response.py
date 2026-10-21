from uuid import UUID

from pydantic import BaseModel


class StudyYearInfo(BaseModel):
    id: UUID
    code: str
    name: str


class AppStateResponse(BaseModel):
    current_selected_study_year: StudyYearInfo | None
