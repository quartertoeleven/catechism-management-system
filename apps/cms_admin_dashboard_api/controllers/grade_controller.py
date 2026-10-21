from uuid import UUID

from cms_locale import Translator
from containers import ApplicationContainer
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Response
from handlers.create_grade_handler import CreateGradeHandler
from handlers.delete_grade_handler import DeleteGradeHandler
from handlers.get_grade_handler import GetGradeHandler
from handlers.list_grades_handler import ListGradesHandler
from handlers.update_grade_handler import UpdateGradeHandler
from logto import IdTokenClaims
from models.create_grade_request import CreateGradeRequest
from models.create_grade_response import CreateGradeResponse
from models.get_grade_response import GetGradeResponse
from models.list_grades_response import ListGradesResponse
from models.update_grade_request import UpdateGradeRequest
from models.update_grade_response import UpdateGradeResponse

from dependencies.auth_dependency import get_authenticated_user
from dependencies.locale_dependency import get_locale_translator

router = APIRouter(prefix="/grades", tags=["grades"])


@router.get("")
@inject
async def list_grades(
    study_year_code: str | None = Query(default=None),
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: ListGradesHandler = Depends(
        Provide[ApplicationContainer.list_grades_handler]
    ),
) -> ListGradesResponse:
    return await handler(study_year_code, translator)


@router.get("/{grade_id}")
@inject
async def get_grade(
    grade_id: UUID,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: GetGradeHandler = Depends(Provide[ApplicationContainer.get_grade_handler]),
) -> GetGradeResponse:
    return await handler(grade_id, translator)


@router.put("/{grade_id}")
@inject
async def update_grade(
    grade_id: UUID,
    body: UpdateGradeRequest,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: UpdateGradeHandler = Depends(
        Provide[ApplicationContainer.update_grade_handler]
    ),
) -> UpdateGradeResponse:
    return await handler(grade_id, body, translator)


@router.delete("/{grade_id}")
@inject
async def delete_grade(
    grade_id: UUID,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: DeleteGradeHandler = Depends(
        Provide[ApplicationContainer.delete_grade_handler]
    ),
) -> Response:
    return await handler(grade_id, translator)


@router.post("")
@inject
async def create_grade(
    body: CreateGradeRequest,
    claims: IdTokenClaims = Depends(get_authenticated_user),
    translator: Translator = Depends(get_locale_translator),
    handler: CreateGradeHandler = Depends(
        Provide[ApplicationContainer.create_grade_handler]
    ),
) -> CreateGradeResponse:
    return await handler(body, translator)
