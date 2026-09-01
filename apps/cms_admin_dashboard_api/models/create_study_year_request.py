from pydantic import BaseModel


class CreateStudyYearRequest(BaseModel):
    code: str
    name: str
    is_current: bool
    is_readonly: bool
    subject: str | None = None
    bible_sentence: str | None = None
    description: str | None = None
