from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from handlers.app_state_handler import AppStateHandler
from logto import IdTokenClaims
from models.app_state_response import AppStateResponse

from dependencies.auth_dependency import get_authenticated_user

router = APIRouter(prefix="/app-state", tags=["app-state"])


@router.get("")
@inject
async def get_app_state(
    claims: IdTokenClaims = Depends(get_authenticated_user),
    handler: AppStateHandler = Depends(Provide[ApplicationContainer.app_state_handler]),
) -> AppStateResponse:
    return await handler()
