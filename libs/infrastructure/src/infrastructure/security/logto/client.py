"""Logto identity provider adapter."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
from urllib.parse import urlencode

import httpx2
from application.common.auth.errors import AuthenticationError
from application.common.auth.models import TokenSet, UserProfile
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.oauth2.rfc7636 import create_s256_code_challenge
from joserfc import jwt
from joserfc.errors import JoseError
from joserfc.jwk import KeySet
from joserfc.jwt import JWTClaimsRegistry

from infrastructure.security.constants import (
    ID_TOKEN_LEEWAY_SECONDS,
    PKCE_CODE_CHALLENGE_METHOD,
)
from infrastructure.security.logto.discovery import OidcDiscovery, OidcMetadata
from infrastructure.security.logto.settings import LogtoSettings

AUTHORIZATION_CODE_RESPONSE_TYPE: str = "code"
BEARER_PREFIX: str = "Bearer "


class LogtoIdentityProvider:
    """Implement the identity provider port with Logto."""

    def __init__(
        self,
        settings: LogtoSettings,
        discovery: OidcDiscovery,
        http_client: httpx2.AsyncClient,
    ) -> None:
        self._settings = settings
        self._discovery = discovery
        self._http_client = http_client

    async def authorization_url(
        self, *, state: str, nonce: str, code_verifier: str
    ) -> str:
        """Build the Logto authorization URL."""
        metadata = await self._discovery.metadata()
        params = {
            "client_id": self._settings.app_id,
            "redirect_uri": self._settings.redirect_uri,
            "response_type": AUTHORIZATION_CODE_RESPONSE_TYPE,
            "scope": " ".join(self._settings.scope_list),
            "state": state,
            "nonce": nonce,
            "code_challenge": create_s256_code_challenge(code_verifier),
            "code_challenge_method": PKCE_CODE_CHALLENGE_METHOD,
        }
        return f"{metadata.authorization_endpoint}?{urlencode(params)}"

    async def exchange_code(
        self, *, code: str, code_verifier: str, nonce: str
    ) -> TokenSet:
        """Exchange an authorization code for tokens."""
        metadata = await self._discovery.metadata()
        client = self._oauth_client()
        try:
            token = await client.fetch_token(
                metadata.token_endpoint,
                code=code,
                code_verifier=code_verifier,
            )
        except Exception as exc:
            raise AuthenticationError("Token exchange failed") from exc
        finally:
            await client.aclose()

        await self._verify_id_token(
            token.get("id_token"),
            nonce=nonce,
            metadata=metadata,
        )
        return _to_token_set(token)

    async def refresh(self, *, refresh_token: str) -> TokenSet:
        """Exchange a refresh token for a new token set."""
        metadata = await self._discovery.metadata()
        client = self._oauth_client()
        try:
            token = await client.refresh_token(
                metadata.token_endpoint,
                refresh_token=refresh_token,
            )
        except Exception as exc:
            raise AuthenticationError("Token refresh failed") from exc
        finally:
            await client.aclose()

        return _to_token_set(token)

    async def userinfo(self, *, access_token: str) -> UserProfile:
        """Fetch user profile claims."""
        metadata = await self._discovery.metadata()
        try:
            response = await self._http_client.get(
                metadata.userinfo_endpoint,
                headers={"Authorization": f"{BEARER_PREFIX}{access_token}"},
            )
            response.raise_for_status()
            payload = response.json()
        except (httpx2.HTTPError, ValueError) as exc:
            raise AuthenticationError("Userinfo request failed") from exc

        if not isinstance(payload, dict) or "sub" not in payload:
            raise AuthenticationError("Invalid userinfo response")

        return UserProfile(
            subject=str(payload["sub"]),
            name=_optional_string(payload.get("name")),
            email=_optional_string(payload.get("email")),
            picture=_optional_string(payload.get("picture")),
        )

    async def end_session_url(self, *, id_token: str | None) -> str:
        """Build the Logto logout URL."""
        metadata = await self._discovery.metadata()
        params = {
            "post_logout_redirect_uri": self._settings.post_logout_redirect_uri,
        }
        if id_token:
            params["id_token_hint"] = id_token
        return f"{metadata.end_session_endpoint}?{urlencode(params)}"

    def _oauth_client(self) -> AsyncOAuth2Client:
        return AsyncOAuth2Client(
            client_id=self._settings.app_id,
            client_secret=self._settings.app_secret,
            redirect_uri=self._settings.redirect_uri,
            scope=" ".join(self._settings.scope_list),
        )

    async def _verify_id_token(
        self,
        id_token: str | None,
        *,
        nonce: str,
        metadata: OidcMetadata,
    ) -> None:
        if not id_token:
            raise AuthenticationError("Missing ID token")

        jwks = await self._discovery.jwks()
        registry = JWTClaimsRegistry(
            leeway=ID_TOKEN_LEEWAY_SECONDS,
            iss={"essential": True, "value": metadata.issuer},
            aud={"essential": True, "value": self._settings.app_id},
            nonce={"essential": True, "value": nonce},
            exp={"essential": True},
            iat={"essential": True},
            sub={"essential": True},
        )
        try:
            key_set = KeySet.import_key_set(jwks)
            token = jwt.decode(
                id_token,
                key_set,
                algorithms=metadata.id_token_signing_alg_values_supported,
            )
            registry.validate(token.claims)
        except (JoseError, ValueError) as exc:
            raise AuthenticationError("Invalid ID token") from exc


def _to_token_set(token: dict[str, Any]) -> TokenSet:
    try:
        access_token = str(token["access_token"])
        expires_at = _expires_at(token)
    except (KeyError, TypeError, ValueError) as exc:
        raise AuthenticationError("Invalid token response") from exc

    return TokenSet(
        access_token=access_token,
        refresh_token=_optional_string(token.get("refresh_token")),
        id_token=_optional_string(token.get("id_token")),
        expires_at=expires_at,
    )


def _expires_at(token: dict[str, Any]) -> datetime:
    expires_at = token.get("expires_at")
    if expires_at is not None:
        return datetime.fromtimestamp(float(expires_at), tz=UTC)

    expires_in = float(token["expires_in"])
    return datetime.now(tz=UTC) + timedelta(seconds=expires_in)


def _optional_string(value: object) -> str | None:
    return None if value is None else str(value)
