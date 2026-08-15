from logto import LogtoClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from cms_common.integrations.logto import LogtoAuthClient
from cms_common.profile.models.user_profile import UserProfile
from cms_common.profile.services.profile_service import ProfileService


class ProfileHandler:
    def __init__(
        self,
        logto_auth_client: LogtoAuthClient,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._logto_auth_client = logto_auth_client
        self._session_factory = session_factory

    async def get_user_profile(self, client: LogtoClient) -> UserProfile:
        user_info = await self._logto_auth_client.get_user_info(client)
        async with self._session_factory() as session:
            return await ProfileService.build_profile(user_info, session)
