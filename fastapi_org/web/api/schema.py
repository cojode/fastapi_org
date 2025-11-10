from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from dataclasses import fields

from pydantic_core import PydanticCustomError

from fastapi_org.domain.location import (
    LocationShape,
    CircleLocation,
    RectLocation,
    SupportedShapedLocations,
)


from fastapi_org.exceptions import NotFoundError


class BaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GenericResponseMessageField(BaseModel):
    msg: str = Field(default="success")


class GenericResponse[T](GenericResponseMessageField):
    data: list[T] | T | None

    @field_validator("data", mode="before")
    @classmethod
    def convert_to_single_value(cls, v) -> T | None:
        if isinstance(v, list):
            if len(v) == 0:
                return None
            if len(v) == 1:
                return v[0]
            raise ValidationError(
                "Response expected to have a single item, but more were provided.",
            )
        return v

    @field_validator("data", mode="after")
    @classmethod
    def auto_404(cls, v):
        if v is None:
            raise NotFoundError
        return v


class GenericListResponse[T](GenericResponseMessageField):
    values: list[T] | T | None
    count: int = Field(default_factory=lambda r: len(r["values"]))

    @field_validator("values", mode="before")
    @classmethod
    def convert_to_list(cls, v) -> list[T]:
        if v is None:
            return []
        if not isinstance(v, list):
            return [v]
        return v


class WithLocationParams(BaseModel):
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
                raise ValueError(
                    f"Unknown location shape: {self.location_shape}"
                )
        return self
