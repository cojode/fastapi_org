from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from fastapi_org.dependency import (
    get_get_organization_by_id_use_case,
    get_search_organizations_use_case,
)
from fastapi_org.services.organization.base import OrganizationUseCase
from fastapi_org.web.api.organization.schema import (
    MultipleOrganizationResponse,
    SearchOrganizationsParams,
    SingleOrganizationResponse,
    get_search_params,
)

router = APIRouter()


@router.get("", response_model=MultipleOrganizationResponse)
async def search_org(
    params: SearchOrganizationsParams = Depends(get_search_params),
    use_case: OrganizationUseCase = Depends(get_search_organizations_use_case),
):
    return MultipleOrganizationResponse(values=await use_case.execute(params))


@router.get("/{id}", response_model=SingleOrganizationResponse)
async def get_org_by_id(
    id: PositiveInt,
    use_case: OrganizationUseCase = Depends(
        get_get_organization_by_id_use_case
    ),
):
    return SingleOrganizationResponse(data=await use_case.execute(id))
