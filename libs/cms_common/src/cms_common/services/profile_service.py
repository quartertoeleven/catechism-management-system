from typing import TYPE_CHECKING

from logto import LogtoClient, UserInfoResponse
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from cms_common.models.user_profile import UserCustomData, UserInfoData
from cms_common.services.catechist_service import CatechistService

if TYPE_CHECKING:
    from cms_integrations.logto import LogtoService


class ProfileService:
    def __init__(
        self,
        logto_service: "LogtoService",
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._logto_service = logto_service
        self._session_factory = session_factory

    async def my_profile(self, client: LogtoClient) -> UserInfoData:
        user_info = await self._logto_service.get_user_info(client)
        async with self._session_factory() as session:
            return await self._build_profile(user_info, session)

    @staticmethod
    async def _build_profile(
        user_info: UserInfoResponse, session: AsyncSession
    ) -> UserInfoData:
        custom_data = UserCustomData.model_validate(user_info.custom_data or {})
        catechist = await CatechistService.get_by_code(
            session, custom_data.catechist_code
        )
        return UserInfoData(
            name=user_info.name,
            email=user_info.email,
            catechist=catechist,
        )
