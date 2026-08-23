from pydantic import BaseModel


class CheckResponse(BaseModel):
    authenticated: bool
    sub: str
