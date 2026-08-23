from handlers.base_handler import BaseHandler
from models.health_check_response import HealthCheckResponse


class HealthCheckHandler(BaseHandler):
    def __init__(self, version: str) -> None:
        self._version = version

    def handle(self) -> HealthCheckResponse:
        return HealthCheckResponse(ping="pong", version=self._version)
