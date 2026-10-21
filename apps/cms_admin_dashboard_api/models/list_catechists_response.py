from cms_common.models import CatechistSchema
from pydantic import BaseModel


class ListCatechistsResponse(BaseModel):
    data: list[CatechistSchema]
