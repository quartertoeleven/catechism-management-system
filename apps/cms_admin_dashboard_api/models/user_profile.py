from typing import Optional

from cms_common.models import CatechistSchema
from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    catechist: Optional[CatechistSchema] = None
