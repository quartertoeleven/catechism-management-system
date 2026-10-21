from uuid import UUID

from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from handlers.list_catechists_handler import ListCatechistsHandler
from logto import IdTokenClaims
from models.list_catechists_response import ListCatechistsResponse

from dependencies.auth_dependency import get_authenticated_user

router = APIRouter(prefix="/catechists", tags=["catechists"])


@router.get("")
@inject
async def list_catechists(
    query: str | None = Query(default=None),
    ids: list[UUID] | None = Query(default=None),
    claims: IdTokenClaims = Depends(get_authenticated_user),
    handler: ListCatechistsHandler = Depends(
        Provide[ApplicationContainer.list_catechists_handler]
    ),
) -> ListCatechistsResponse:
    return await handler(query, ids)
