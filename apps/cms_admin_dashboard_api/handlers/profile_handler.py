from cms_common.services import ProfileService
from fastapi import Request
from handlers.base_handler import BaseAsyncHandler
from models.user_profile import UserProfileResponse
from services.auth_service import AuthService


class ProfileHandler(BaseAsyncHandler):
    def __init__(
        self,
        auth_service: AuthService,
        profile_service: ProfileService,
    ) -> None:
        self._auth_service = auth_service
        self._profile_service = profile_service

    async def handle(self, request: Request) -> UserProfileResponse:
        client = self._auth_service.create_client(request)
        data = await self._profile_service.my_profile(client)
        return UserProfileResponse(
            name=data.name,
            email=data.email,
            catechist=data.catechist,
        )
