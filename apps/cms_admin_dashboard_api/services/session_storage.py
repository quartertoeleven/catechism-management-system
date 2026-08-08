from typing import Dict, Optional

import jwt
from fastapi import Request
from fastapi.responses import Response
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


class SessionCookieStorage(Storage):
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
    def from_request(
        cls,
        request: Request,
        secret: str,
        cookie_name: str,
        cookie_secure: bool,
        cookie_samesite: str,
        cookie_max_age: int,
    ) -> "SessionCookieStorage":
        return cls(
            _decode_session(request.cookies.get(cookie_name), secret),
            secret,
            cookie_name,
            cookie_secure,
            cookie_samesite,
            cookie_max_age,
        )

    def get(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def set(self, key: str, value: Optional[str]) -> None:
        self._data[key] = value

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def write_to(self, response: Response) -> None:
        if not self._data:
            response.delete_cookie(self._cookie_name)
            return
        response.set_cookie(
            key=self._cookie_name,
            value=_encode_session(self._data, self._secret),
            httponly=True,
            secure=self._cookie_secure,
            samesite=self._cookie_samesite,
            max_age=self._cookie_max_age,
            path="/",
        )
