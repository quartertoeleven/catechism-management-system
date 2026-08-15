from cms_common.health_check.models.health_check_response import HealthCheckResponse
from cms_common.health_check.services.health_service import HealthService


class HealthCheckHandler:
    def __init__(self, health_service: HealthService) -> None:
        self._health_service = health_service

    def get_health_status(self) -> HealthCheckResponse:
        return self._health_service.get_health_status()
