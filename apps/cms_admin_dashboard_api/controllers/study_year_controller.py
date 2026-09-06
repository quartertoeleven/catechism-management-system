from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from handlers.create_study_year_handler import CreateStudyYearHandler
from handlers.list_study_years_handler import ListStudyYearsHandler
from logto import IdTokenClaims
from models.create_study_year_request import CreateStudyYearRequest
from models.create_study_year_response import CreateStudyYearResponse
from models.list_study_years_response import ListStudyYearsResponse

from dependencies.auth_dependency import get_authenticated_user

router = APIRouter(prefix="/study-years", tags=["study-years"])


@router.get("/")
@inject
async def list_study_years(
    claims: IdTokenClaims = Depends(get_authenticated_user),
    list_study_years_handler: ListStudyYearsHandler = Depends(
        Provide[ApplicationContainer.list_study_years_handler]
    ),
) -> ListStudyYearsResponse:
    return await list_study_years_handler()


@router.post("/")
@inject
async def create_study_year(
    body: CreateStudyYearRequest,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    create_study_year_handler: CreateStudyYearHandler = Depends(
        Provide[ApplicationContainer.create_study_year_handler]
    ),
) -> CreateStudyYearResponse:
    return await create_study_year_handler(body)
