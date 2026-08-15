from cms_common.health_check.models.health_check_response import HealthCheckResponse


class HealthService:
    def __init__(self, version: str) -> None:
        self._version = version

    def get_health_status(self) -> HealthCheckResponse:
        return HealthCheckResponse(ping="pong", version=self._version)
