"""Security dependency injection provider."""

from collections.abc import AsyncIterator

import httpx2
from application.common.auth.ports import (
    FlowStore,
    IdentityProvider,
    SessionStore,
)
from application.common.auth.service import AuthenticationService
from cryptography.fernet import Fernet, MultiFernet
from dishka import Provider, Scope, provide
from domain.directory.repositories import CatechistRepository

from infrastructure.security.constants import (
    ENCRYPTION_KEY_SEPARATOR,
    HTTP_TIMEOUT_SECONDS,
)
from infrastructure.security.logto.client import LogtoIdentityProvider
from infrastructure.security.logto.discovery import OidcDiscovery
from infrastructure.security.logto.settings import LogtoSettings
from infrastructure.security.session.cookie import (
    EncryptedCookieFlowStore,
    EncryptedCookieSessionStore,
)


class SecurityProvider(Provider):
    """Provide authentication services."""

    @provide(scope=Scope.APP)
    def settings(self) -> LogtoSettings:
        """Build Logto settings from the environment."""
        return LogtoSettings()

    @provide(scope=Scope.APP)
    async def http_client(self) -> AsyncIterator[httpx2.AsyncClient]:
        """Provide a shared HTTP client."""
        async with httpx2.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS) as client:
            yield client

    @provide(scope=Scope.APP)
    def fernet(self, settings: LogtoSettings) -> MultiFernet:
        """Build the cookie encryption helper."""
        keys = [
            Fernet(key.strip().encode())
            for key in settings.session_encryption_key.split(ENCRYPTION_KEY_SEPARATOR)
            if key.strip()
        ]
        if not keys:
            raise ValueError("SESSION_ENCRYPTION_KEY must not be empty")
        return MultiFernet(keys)

    @provide(scope=Scope.APP)
    def discovery(
        self,
        client: httpx2.AsyncClient,
        settings: LogtoSettings,
    ) -> OidcDiscovery:
        """Provide the OIDC discovery cache."""
        return OidcDiscovery(client, settings)

    @provide(scope=Scope.REQUEST)
    def identity_provider(
        self,
        settings: LogtoSettings,
        discovery: OidcDiscovery,
        client: httpx2.AsyncClient,
    ) -> IdentityProvider:
        """Provide the Logto identity provider."""
        return LogtoIdentityProvider(
            settings=settings,
            discovery=discovery,
            http_client=client,
        )

    @provide(scope=Scope.REQUEST)
    def session_store(self, fernet: MultiFernet) -> SessionStore:
        """Provide the session cookie codec."""
        return EncryptedCookieSessionStore(fernet)

    @provide(scope=Scope.REQUEST)
    def flow_store(self, fernet: MultiFernet) -> FlowStore:
        """Provide the flow cookie codec."""
        return EncryptedCookieFlowStore(fernet)

    @provide(scope=Scope.REQUEST)
    def authentication_service(
        self,
        provider: IdentityProvider,
        catechists: CatechistRepository,
    ) -> AuthenticationService:
        """Provide the authentication service."""
        return AuthenticationService(provider, catechists)
