from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from handlers.create_study_year_handler import CreateStudyYearHandler
from logto import IdTokenClaims
from models.create_study_year_request import CreateStudyYearRequest
from models.create_study_year_response import CreateStudyYearResponse

from dependencies.auth_dependency import get_authenticated_user

router = APIRouter(prefix="/study-years", tags=["study-years"])


@router.post("/")
@inject
async def create_study_year(
    body: CreateStudyYearRequest = ...,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    create_study_year_handler: CreateStudyYearHandler = Depends(
        Provide[ApplicationContainer.create_study_year_handler]
    ),
) -> CreateStudyYearResponse:
    return await create_study_year_handler(body)
