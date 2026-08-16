from typing import Protocol


class LocaleServiceProtocol(Protocol):
    def gettext(self, domain: str, locale: str, msgid: str) -> str: ...

    def ngettext(
        self, domain: str, locale: str, msgid: str, plural: str, n: int
    ) -> str: ...


class Translator:
    """Bound-domain facade over a locale service.

    Callers keep a :class:`Translator` for a domain, pass the locale once,
    and then translate without repeating the domain/locale on every call.
    """

    def __init__(
        self, service: LocaleServiceProtocol, domain: str, locale: str
    ) -> None:
        self._service = service
        self._domain = domain
        self._locale = locale

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def locale(self) -> str:
        return self._locale

    @property
    def service(self) -> LocaleServiceProtocol:
        return self._service

    def gettext(self, msgid: str) -> str:
        return self._service.gettext(self._domain, self._locale, msgid)

    def ngettext(self, msgid: str, plural: str, n: int) -> str:
        return self._service.ngettext(
            self._domain, self._locale, msgid, plural, n
        )
