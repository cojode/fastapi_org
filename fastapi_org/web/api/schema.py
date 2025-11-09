
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
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
