from typing import Any

from fastapi_org.services.building.base import Building, BuildingUseCase


class SearchBuildingsUseCase(BuildingUseCase):

    async def execute(self, *args: Any, **kwargs: Any) -> list[Building]:
        params = kwargs.get("params") or args[0]

        return await self.building_repo.search(
            location=params.location,
        )
