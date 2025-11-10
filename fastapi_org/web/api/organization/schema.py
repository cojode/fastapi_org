from pydantic import PositiveInt

from fastapi_org.domain.organization import (
    Organization,
)

from fastapi_org.web.api.schema import (
    GenericListResponse,
    GenericResponse,
    WithLocationParams,
)


class SearchOrganizationsParams(WithLocationParams):
    organization_name: str | None = None
    building_id: PositiveInt | None = None

    activity_id: PositiveInt | None = None
    recursive_activity: bool = False


class SingleOrganizationResponse(GenericResponse[Organization]): ...


class MultipleOrganizationResponse(GenericListResponse[Organization]): ...
