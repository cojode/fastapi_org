from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_org.domain.organization import (
    OrganizaitonRepository,
)


class SQLAlchemyOrganizationRepository(OrganizaitonRepository):
    """SQLAlchemy implementation of the OrganizationRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
