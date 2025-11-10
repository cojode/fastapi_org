from fastapi_org.web.api.schema import GenericListResponse, WithLocationParams

from fastapi_org.domain.building import Building


class SearchBuildingsParams(WithLocationParams): ...


class MultipleBuildingResponse(GenericListResponse[Building]): ...
