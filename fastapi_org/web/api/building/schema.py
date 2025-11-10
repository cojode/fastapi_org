from fastapi_org.domain.building import Building
from fastapi_org.web.api.schema import GenericListResponse, WithLocationParams


class SearchBuildingsParams(WithLocationParams): ...


class MultipleBuildingResponse(GenericListResponse[Building]): ...
