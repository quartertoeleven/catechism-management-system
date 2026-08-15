from logto import UserInfoResponse
from sqlalchemy.ext.asyncio import AsyncSession

from cms_common.catechist.services.catechist_service import CatechistService
from cms_common.profile.models.user_profile import UserCustomData, UserProfile


class ProfileService:
    @staticmethod
    async def build_profile(
        user_info: UserInfoResponse, session: AsyncSession
    ) -> UserProfile:
        custom_data = UserCustomData.model_validate(user_info.custom_data or {})
        catechist = await CatechistService.get_by_code(
            session, custom_data.catechist_code
        )
        return UserProfile(
            name=user_info.name,
            email=user_info.email,
            catechist=catechist,
        )
