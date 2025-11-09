from fastapi import Depends
from fastapi_org.db.dependencies import get_db_session

from fastapi_org.db.repos.organization import SQLAlchemyOrganizationRepository
from fastapi_org.domain.organization import OrganizaitonRepository

from fastapi_org.services.organization import (
    GetOrganizationByIdUseCase,
    SearchOrganizationsUseCase,
)

from fastapi_org.services.organization.base import OrganizationUseCase


def get_org_repo(session=Depends(get_db_session)) -> OrganizaitonRepository:
    return SQLAlchemyOrganizationRepository(session)


def get_search_organizations_use_case(
    repo: OrganizaitonRepository = Depends(get_org_repo),
) -> OrganizationUseCase:
    return SearchOrganizationsUseCase(org_repo=repo)


def get_get_organization_by_id_use_case(
    repo: OrganizaitonRepository = Depends(get_org_repo),
) -> OrganizationUseCase:
    return GetOrganizationByIdUseCase(org_repo=repo)
