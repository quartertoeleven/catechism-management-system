import gettext
from gettext import GNUTranslations
from pathlib import Path

from cms_locale.core.exceptions import MissingCatalogError, UnsupportedLocaleError
from cms_locale.core.models.locale_config import LocaleConfig
from cms_locale.core.services.translator import Translator


class LocaleService:
    """Loads and caches gettext catalogs keyed by (domain, locale).

    Catalogs are expected at
    ``<catalogs_dir>/<locale>/LC_MESSAGES/<domain>.mo``.
    """

    def __init__(self, config: LocaleConfig) -> None:
        self._config = config
        self._catalogs: dict[tuple[str, str], GNUTranslations] = {}

    @property
    def config(self) -> LocaleConfig:
        return self._config

    def _catalog_path(self, domain: str, locale: str) -> Path:
        return (
            self._config.catalogs_dir
            / locale
            / "LC_MESSAGES"
            / f"{domain}.mo"
        )

    def _validate_locale(self, locale: str) -> None:
        if locale not in self._config.supported_locales:
            raise UnsupportedLocaleError(f"Unsupported locale: {locale}")

    def _load(self, domain: str, locale: str) -> GNUTranslations:
        key = (domain, locale)
        cached = self._catalogs.get(key)
        if cached is not None:
            return cached

        self._validate_locale(locale)
        path = self._catalog_path(domain, locale)
        if not path.exists():
            raise MissingCatalogError(f"Missing catalog: {path}")

        translation = gettext.translation(
            domain,
            self._config.catalogs_dir,
            languages=[locale],
            fallback=False,
        )
        self._catalogs[key] = translation
        return translation

    def gettext(self, domain: str, locale: str, msgid: str) -> str:
        return self._load(domain, locale).gettext(msgid)

    def ngettext(
        self, domain: str, locale: str, msgid: str, plural: str, n: int
    ) -> str:
        return self._load(domain, locale).ngettext(msgid, plural, n)

    def locales(self, domain: str) -> tuple[str, ...]:
        return tuple(
            locale
            for locale in self._config.supported_locales
            if self._catalog_path(domain, locale).exists()
        )

    def get_translator(
        self, domain: str, locale: str | None = None
    ) -> Translator:
        return Translator(self, domain, locale or self._config.default_locale)

    def resolve_locale(self, accept_language: str | None) -> str:
        """Pick best supported locale from an ``Accept-Language`` header.

        Uses q-value ranking; ties keep client ordering. Falls back to
        ``default_locale`` when the header is absent and to
        ``fallback_locale`` when no supported locale matches.
        """
        if not accept_language:
            return self._config.default_locale

        supported = {locale.lower() for locale in self._config.supported_locales}
        best_match: str | None = None
        best_q = -1.0

        for part in accept_language.split(","):
            part = part.strip()
            if not part:
                continue

            tag = part.split(";")[0].strip()
            q = 1.0
            for token in part.split(";")[1:]:
                token = token.strip()
                if token.lower().startswith("q="):
                    try:
                        q = float(token[2:])
                    except ValueError:
                        q = 0.0

            base = tag.split("-")[0].strip().lower()
            if not base or base not in supported:
                continue

            if q > best_q:
                best_q = q
                best_match = base

        if best_match is not None:
            return best_match
        return self._config.fallback_locale or self._config.default_locale
