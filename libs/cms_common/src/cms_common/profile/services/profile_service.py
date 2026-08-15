from logto import LogtoClient, UserInfoResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from cms_common.catechist.services.catechist_service import CatechistService
from cms_common.integrations.logto import LogtoAuthClient
from cms_common.profile.models.user_profile import UserCustomData, UserProfileResponse


class ProfileService:
    def __init__(
        self,
        logto_auth_client: LogtoAuthClient,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._logto_auth_client = logto_auth_client
        self._session_factory = session_factory

    async def my_profile(self, client: LogtoClient) -> UserProfileResponse:
        user_info = await self._logto_auth_client.get_user_info(client)
        async with self._session_factory() as session:
            return await self._build_profile(user_info, session)

    @staticmethod
    async def _build_profile(
        user_info: UserInfoResponse, session: AsyncSession
    ) -> UserProfileResponse:
        custom_data = UserCustomData.model_validate(user_info.custom_data or {})
        catechist = await CatechistService.get_by_code(
            session, custom_data.catechist_code
        )
        return UserProfileResponse(
            name=user_info.name,
            email=user_info.email,
            catechist=catechist,
        )
