from fastapi_org.web.api.dependency import LocationParams
from fastapi_org.web.api.building.schema import SearchBuildingsParams
from pydantic import ValidationError
from fastapi import Depends
from fastapi.exceptions import RequestValidationError


def get_search_building_params(
    location: LocationParams = Depends(),
) -> SearchBuildingsParams:
    try:
        return SearchBuildingsParams(
            location_shape=location.location_shape,
            center_la=location.center_la,
            center_lo=location.center_lo,
            radius=location.radius,
            first_la=location.first_la,
            first_lo=location.first_lo,
            second_la=location.second_la,
            second_lo=location.second_lo,
        )
    except ValidationError as e:
        raise RequestValidationError(e.errors()) from e
