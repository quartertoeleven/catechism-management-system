from cms_integrations.logto import LogtoSessionCookieStorage
from fastapi import Request
from fastapi.responses import Response


class FastAPISessionCookieStorage(LogtoSessionCookieStorage):
    @classmethod
    def from_request(
        cls,
        request: Request,
        secret: str,
        cookie_name: str,
        cookie_secure: bool,
        cookie_samesite: str,
        cookie_max_age: int,
    ) -> "LogtoSessionCookieStorage":
        return cls.from_cookies(
            request.cookies,
            secret,
            cookie_name,
            cookie_secure,
            cookie_samesite,
            cookie_max_age,
        )

    def write_to(self, response: Response) -> None:
        if self.is_empty:
            response.delete_cookie(self.cookie_name)
            return
        response.set_cookie(
            key=self.cookie_name,
            value=self.serialize(),
            httponly=True,
            secure=self.cookie_secure,
            samesite=self.cookie_samesite,
            max_age=self.cookie_max_age,
            path="/",
        )
