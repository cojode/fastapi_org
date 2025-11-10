from fastapi import APIRouter, Depends

from fastapi_org.dependency import (
    get_search_building_use_case,
)

from fastapi_org.services.building.base import BuildingUseCase
from fastapi_org.web.api.building.schema import (
    MultipleBuildingResponse,
    SearchBuildingsParams,
)
from fastapi_org.web.api.building.dependency import get_search_building_params

router = APIRouter()


@router.get("", response_model=MultipleBuildingResponse)
async def search_building(
    params: SearchBuildingsParams = Depends(get_search_building_params),
    use_case: BuildingUseCase = Depends(get_search_building_use_case),
):
    print(params)
    return MultipleBuildingResponse(values=await use_case.execute(params))
