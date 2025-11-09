from fastapi_org.services.organization.base import OrganizationUseCase


class GetOrganizationByIdUseCase(OrganizationUseCase):
    async def execute(self, *args, **kwargs):
        """
        Args:
            organization_id (int): id of organization to obtain
        """
        return (
            await self.org_repo.get_by_id(
                organization_id=kwargs.get("organization_id") or args[0]
            )
            or []
        )
