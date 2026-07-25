class HealthService:
    def __init__(self, version: str) -> None:
        self._version = version

    def get_health_status(self) -> dict:
        return {"ping": "pong", "version": self._version}
