from logto import UserInfoResponse

from cms_common.profile.models.user_profile import UserProfile


class ProfileService:
    @staticmethod
    def build_profile(user_info: UserInfoResponse) -> UserProfile:
        return UserProfile(
            name=user_info.name,
            email=user_info.email,
            custom_data=user_info.custom_data,
        )