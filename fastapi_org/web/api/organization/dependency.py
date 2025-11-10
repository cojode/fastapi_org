from fastapi_org.web.api.dependency import LocationParams
from fastapi_org.web.api.organization.schema import SearchOrganizationsParams
from pydantic import ValidationError
from fastapi import Query, Depends
from fastapi.exceptions import RequestValidationError


def get_search_org_params(
    organization_name: str | None = Query(
        None, description="Organization name"
    ),
    building_id: int | None = Query(
        None, gt=0, description="Building ID (must be a positive integer)"
    ),
    activity_id: int | None = Query(
        None, gt=0, description="Activity ID (must be a positive integer)"
    ),
    recursive_activity: bool = Query(
        False, description="Include nested activities if True"
    ),
    location: LocationParams = Depends(),
) -> SearchOrganizationsParams:
    try:
        return SearchOrganizationsParams(
            organization_name=organization_name,
            building_id=building_id,
            activity_id=activity_id,
            recursive_activity=recursive_activity,
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
