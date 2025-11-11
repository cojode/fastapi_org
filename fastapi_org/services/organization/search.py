from typing import Any

from fastapi_org.services.organization.base import (
    Organization,
    OrganizationUseCase,
)


class SearchOrganizationsUseCase(OrganizationUseCase):

    async def execute(self, *args: Any, **kwargs: Any) -> list[Organization]:
        params = kwargs.get("params") or args[0]

        return await self.org_repo.search(
            organization_name=params.organization_name,
            building_id=params.building_id,
            activity_id=params.activity_id,
            recursive_activity=params.recursive_activity,
            location=params.location,
        )
