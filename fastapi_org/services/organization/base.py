from fastapi_org.domain.organization import (
    OrganizaitonRepository,
    Organization,
)
from fastapi_org.services.base import UseCaseProtocol


class OrganizationUseCase(UseCaseProtocol[Organization]):
    def __init__(self, org_repo: OrganizaitonRepository) -> None:
        self.org_repo = org_repo
