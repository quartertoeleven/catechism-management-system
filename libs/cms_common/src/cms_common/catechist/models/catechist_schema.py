from uuid import UUID

from pydantic import BaseModel

from cms_db_models.enums import CatechistTitle, Gender


class CatechistSchema(BaseModel):
    id: UUID
    code: str
    title: CatechistTitle
    saint_name: str | None = None
    first_name: str
    middle_name: str | None = None
    last_name: str
    gender: Gender