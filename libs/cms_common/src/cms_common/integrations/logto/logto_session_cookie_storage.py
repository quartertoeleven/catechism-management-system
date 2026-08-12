from typing import Dict, Mapping, Optional

import jwt
from logto.Storage import Storage


def _encode_session(data: Dict[str, str], secret: str) -> str:
    return jwt.encode(data, secret, algorithm="HS256")


def _decode_session(cookie_value: Optional[str], secret: str) -> Dict[str, str]:
    if not cookie_value:
        return {}
    try:
        payload = jwt.decode(cookie_value, secret, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return {}
    return {key: value for key, value in payload.items() if isinstance(value, str)}


class LogtoSessionCookieStorage(Storage):
    def __init__(
        self,
        data: Dict[str, str],
        secret: str,
        cookie_name: str,
        cookie_secure: bool,
        cookie_samesite: str,
        cookie_max_age: int,
    ) -> None:
        self._data = data
        self._secret = secret
        self._cookie_name = cookie_name
        self._cookie_secure = cookie_secure
        self._cookie_samesite = cookie_samesite
        self._cookie_max_age = cookie_max_age

    @classmethod
    def from_cookies(
        cls,
        cookies: Mapping[str, str],
        secret: str,
        cookie_name: str,
        cookie_secure: bool,
        cookie_samesite: str,
        cookie_max_age: int,
    ) -> "LogtoSessionCookieStorage":
        return cls(
            _decode_session(cookies.get(cookie_name), secret),
            secret,
            cookie_name,
            cookie_secure,
            cookie_samesite,
            cookie_max_age,
        )

    @property
    def cookie_name(self) -> str:
        return self._cookie_name

    @property
    def cookie_secure(self) -> bool:
        return self._cookie_secure

    @property
    def cookie_samesite(self) -> str:
        return self._cookie_samesite

    @property
    def cookie_max_age(self) -> int:
        return self._cookie_max_age

    @property
    def is_empty(self) -> bool:
        return not self._data

    def serialize(self) -> str:
        return _encode_session(self._data, self._secret)

    def get(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def set(self, key: str, value: Optional[str]) -> None:
        self._data[key] = value

    def delete(self, key: str) -> None:
        self._data.pop(key, None)