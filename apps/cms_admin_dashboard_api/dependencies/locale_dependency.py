from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from cms_locale import LocaleService, Translator

from containers import ApplicationContainer

LOCALE_DOMAIN = "cms_admin_dashboard_api"


@inject
def get_locale_translator(
    request: Request,
    locale_service: LocaleService = Depends(
        Provide[ApplicationContainer.locale_service]
    ),
) -> Translator:
    locale = locale_service.resolve_locale(
        request.headers.get("accept-language")
    )
    return locale_service.get_translator(LOCALE_DOMAIN, locale)
