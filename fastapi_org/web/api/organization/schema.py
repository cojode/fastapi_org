from dataclasses import fields

from fastapi import Query
from fastapi.exceptions import RequestValidationError
from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    ValidationError,
    model_validator,
)
from pydantic_core import PydanticCustomError

from fastapi_org.domain.organization import (
    CircleLocation,
    LocationShape,
    Organization,
    RectLocation,
    SupportedShapedLocations,
)
from fastapi_org.web.api.schema import GenericListResponse, GenericResponse


class SearchOrganizationsParams(BaseModel):
    organization_name: str | None = None
    building_id: PositiveInt | None = None

    activity_id: PositiveInt | None = None
    recursive_activity: bool = False

    location_shape: LocationShape | None = None

    center_la: float | None = None
    center_lo: float | None = None
    radius: float | None = Field(None, gt=0)

    first_la: float | None = None
    first_lo: float | None = None
    second_la: float | None = None
    second_lo: float | None = None

    location: SupportedShapedLocations | None = Field(default=None, init=False)

    @model_validator(mode="after")
    def build_location(self):
        def obtain_location(location_type: type):
            required_keys = [f.name for f in fields(location_type)]
            values = {key: getattr(self, key) for key in required_keys}

            if not all(values.values()):
                raise PydanticCustomError(
                    "missing_shape_fields",
                    "For shape [{location_shape}] you must provide all of: {required_keys}. Missing: {missing}",
                    {
                        "location_shape": self.location_shape,
                        "required_keys": required_keys,
                        "missing": [k for k, v in values.items() if v is None],
                    },
                )
            return location_type(**values)

        match self.location_shape:
            case LocationShape.CIRCLE:
                self.location = obtain_location(CircleLocation)
            case LocationShape.RECTANGULAR:
                self.location = obtain_location(RectLocation)
            case None:
                ...
            case _:
                raise ValueError(f"Unknown location shape: {self.location_shape}")
        return self


def get_search_params(
    organization_name: str | None = Query(None, description="Organization name"),
    building_id: int | None = Query(
        None, gt=0, description="Building ID (must be a positive integer)",
    ),
    activity_id: int | None = Query(
        None, gt=0, description="Activity ID (must be a positive integer)",
    ),
    recursive_activity: bool = Query(
        False, description="Include nested activities if True",
    ),
    location_shape: LocationShape | None = Query(
        None,
        description="Type of search area: 'circle' or 'rectangular'",
        example=None,
    ),
    center_la: float | None = Query(
        None,
        ge=-90,
        le=90,
        description="Latitude of circle center (degrees, -90 to 90)",
        example=55.751244,
    ),
    center_lo: float | None = Query(
        None,
        ge=-180,
        le=180,
        description="Longitude of circle center (degrees, -180 to 180)",
        example=37.618423,
    ),
    radius: float | None = Query(
        None,
        gt=0,
        description="Radius for circular search in meters (must be > 0)",
        example=1000.0,
    ),
    first_la: float | None = Query(
        None,
        ge=-90,
        le=90,
        description="First latitude corner of rectangle (degrees, -90 to 90)",
        example=55.7,
    ),
    first_lo: float | None = Query(
        None,
        ge=-180,
        le=180,
        description="First longitude corner of rectangle (degrees, -180 to 180)",
        example=37.5,
    ),
    second_la: float | None = Query(
        None,
        ge=-90,
        le=90,
        description="Second latitude corner of rectangle (degrees, -90 to 90)",
        example=55.8,
    ),
    second_lo: float | None = Query(
        None,
        ge=-180,
        le=180,
        description="Second longitude corner of rectangle (degrees, -180 to 180)",
        example=37.7,
    ),
) -> SearchOrganizationsParams:
    try:
        return SearchOrganizationsParams(
            organization_name=organization_name,
            building_id=building_id,
            activity_id=activity_id,
            recursive_activity=recursive_activity,
            location_shape=location_shape,
            center_la=center_la,
            center_lo=center_lo,
            radius=radius,
            first_la=first_la,
            first_lo=first_lo,
            second_la=second_la,
            second_lo=second_lo,
        )
    except ValidationError as e:
        raise RequestValidationError(e.errors()) from e


class SingleOrganizationResponse(GenericResponse[Organization]): ...


class MultipleOrganizationResponse(GenericListResponse[Organization]): ...
