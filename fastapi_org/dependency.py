from fastapi import Depends, HTTPException, status, Security
from fastapi.security import APIKeyHeader

from fastapi_org.db.dependencies import get_db_session
from fastapi_org.db.repos.organization import SQLAlchemyOrganizationRepository
from fastapi_org.domain.organization import OrganizaitonRepository
from fastapi_org.services.organization import (
    GetOrganizationByIdUseCase,
    SearchOrganizationsUseCase,
)
from fastapi_org.services.organization.base import OrganizationUseCase

from fastapi_org.settings import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )


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
