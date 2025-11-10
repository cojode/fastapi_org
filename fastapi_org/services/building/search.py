from fastapi_org.services.building.base import BuildingUseCase


class SearchBuildingsUseCase(BuildingUseCase):
    async def execute(self, *args, **kwargs):
        params = kwargs.get("params") or args[0]

        return await self.building_repo.search(
            location=params.location,
        )
