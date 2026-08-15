from typing import Optional

from logto import LogtoClient, LogtoConfig, Scope, UserInfoScope
from logto.Storage import Storage

DEFAULT_SCOPES: list[Scope] = [
    UserInfoScope.openid,
    UserInfoScope.email,
    UserInfoScope.custom_data,
]


class LogtoClientFactory:
    def __init__(
        self,
        endpoint: str,
        app_id: str,
        app_secret: str,
        scopes: Optional[list[Scope]] = None,
    ) -> None:
        self._config = LogtoConfig(
            endpoint=endpoint,
            appId=app_id,
            appSecret=app_secret,
            scopes=list(scopes if scopes is not None else DEFAULT_SCOPES),
        )

    def create_client(self, storage: Storage) -> LogtoClient:
        return LogtoClient(self._config, storage)