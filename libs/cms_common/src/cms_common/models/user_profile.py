from typing import Optional

from pydantic import BaseModel

from cms_common.models.catechist_schema import CatechistSchema


class UserCustomData(BaseModel):
    catechist_code: Optional[str] = None


class UserInfoData(BaseModel):
    name: str | None = None
    email: str | None = None
    catechist: CatechistSchema | None = None
