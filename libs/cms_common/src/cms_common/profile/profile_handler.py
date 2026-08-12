from logto import LogtoClient

from cms_common.integrations.logto import LogtoAuthClient
from cms_common.profile.models.user_profile import UserProfile
from cms_common.profile.services.profile_service import ProfileService


class ProfileHandler:
    def __init__(self, logto_auth_client: LogtoAuthClient) -> None:
        self._logto_auth_client = logto_auth_client

    async def get_user_profile(self, client: LogtoClient) -> UserProfile:
        user_info = await self._logto_auth_client.get_user_info(client)
        return ProfileService.build_profile(user_info)