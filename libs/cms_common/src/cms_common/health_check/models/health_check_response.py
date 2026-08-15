from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    ping: str
    version: str
