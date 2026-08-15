from typing import Optional

from pydantic import BaseModel

from cms_common.catechist.models.catechist_schema import CatechistSchema


class UserCustomData(BaseModel):
    catechist_code: Optional[str] = None


class UserProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    catechist: Optional[CatechistSchema] = None
