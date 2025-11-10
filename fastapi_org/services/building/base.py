from fastapi_org.domain.building import Building, BuildingRepository
from fastapi_org.services.base import UseCaseProtocol


class BuildingUseCase(UseCaseProtocol[Building]):
    def __init__(self, building_repo: BuildingRepository) -> None:
        self.building_repo = building_repo
