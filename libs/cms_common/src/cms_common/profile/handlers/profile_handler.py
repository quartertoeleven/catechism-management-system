from logto import LogtoClient

from cms_common.profile.models.user_profile import UserProfileResponse
from cms_common.profile.services.profile_service import ProfileService


class ProfileHandler:
    def __init__(self, profile_service: ProfileService) -> None:
        self._profile_service = profile_service

    async def my_profile(self, client: LogtoClient) -> UserProfileResponse:
        return await self._profile_service.my_profile(client)
