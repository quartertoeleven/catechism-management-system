"""OIDC discovery and JWKS cache."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Final

import httpx2
from application.common.auth.errors import AuthenticationError

from infrastructure.security.constants import JWKS_CACHE_TTL_SECONDS
from infrastructure.security.logto.settings import LogtoSettings

METADATA_KEYS: Final[tuple[str, ...]] = (
    "issuer",
    "authorization_endpoint",
    "token_endpoint",
    "userinfo_endpoint",
    "end_session_endpoint",
    "jwks_uri",
)


@dataclass(frozen=True, slots=True)
class OidcMetadata:
    """Relevant OpenID Connect discovery values."""

    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    end_session_endpoint: str
    jwks_uri: str
    id_token_signing_alg_values_supported: tuple[str, ...]


class OidcDiscovery:
    """Fetch and cache OIDC metadata and signing keys."""

    def __init__(self, client: httpx2.AsyncClient, settings: LogtoSettings) -> None:
        self._client = client
        self._settings = settings
        self._metadata: OidcMetadata | None = None
        self._jwks: dict[str, Any] | None = None
        self._jwks_fetched_at: float = 0.0
        self._metadata_lock = asyncio.Lock()
        self._jwks_lock = asyncio.Lock()

    async def metadata(self) -> OidcMetadata:
        """Return cached discovery metadata."""
        if self._metadata is not None:
            return self._metadata

        async with self._metadata_lock:
            if self._metadata is None:
                self._metadata = await self._fetch_metadata()
            return self._metadata

    async def jwks(self, *, force_refresh: bool = False) -> dict[str, Any]:
        """Return cached signing keys, refreshing when stale."""
        is_stale = time.monotonic() - self._jwks_fetched_at > JWKS_CACHE_TTL_SECONDS
        if self._jwks is not None and not force_refresh and not is_stale:
            return self._jwks

        async with self._jwks_lock:
            if self._jwks is not None and not force_refresh and not is_stale:
                return self._jwks

            metadata = await self.metadata()
            try:
                response = await self._client.get(metadata.jwks_uri)
                response.raise_for_status()
                payload = response.json()
            except (httpx2.HTTPError, ValueError) as exc:
                raise AuthenticationError("JWKS request failed") from exc

            if not isinstance(payload, dict) or "keys" not in payload:
                raise AuthenticationError("Invalid JWKS response")

            self._jwks = payload
            self._jwks_fetched_at = time.monotonic()
            return self._jwks

    async def _fetch_metadata(self) -> OidcMetadata:
        try:
            response = await self._client.get(self._settings.discovery_url)
            response.raise_for_status()
            payload = response.json()
        except (httpx2.HTTPError, ValueError) as exc:
            raise AuthenticationError("OIDC discovery request failed") from exc

        if not isinstance(payload, dict):
            raise AuthenticationError("Invalid OIDC discovery response")

        try:
            values = {key: str(payload[key]) for key in METADATA_KEYS}
            signing_algorithms = payload["id_token_signing_alg_values_supported"]
        except KeyError as exc:
            raise AuthenticationError("Incomplete OIDC discovery response") from exc

        if (
            not isinstance(signing_algorithms, list)
            or not signing_algorithms
            or not all(isinstance(algorithm, str) for algorithm in signing_algorithms)
        ):
            raise AuthenticationError("Invalid OIDC discovery response")

        return OidcMetadata(
            **values,
            id_token_signing_alg_values_supported=tuple(signing_algorithms),
        )
