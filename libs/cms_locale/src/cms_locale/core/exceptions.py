class LocaleError(Exception):
    """Base error for all locale-related failures."""


class UnsupportedLocaleError(LocaleError):
    """Raised when a locale is not among the supported locales."""


class MissingCatalogError(LocaleError):
    """Raised when a compiled catalog (.mo) for a locale/domain is missing."""
