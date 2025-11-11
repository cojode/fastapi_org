from typing import Any

from sqlalchemy import and_, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi_org.db.models.building import Building
from fastapi_org.domain.building import Building as DomainBuilding
from fastapi_org.domain.building import (
    BuildingRepository,
)
from fastapi_org.domain.location import ShapedLocation


class SQLAlchemyBuildingRepository(BuildingRepository):
    """SQLAlchemy implementation of the BuildingRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def search(
        self,
        location: ShapedLocation | None = None,
    ) -> list[DomainBuilding]:
        query = select(Building).options(
            joinedload(Building.organizations),
        )
        conditions: list[Any] = []
        query_params: dict[str, Any] = {}

        if location is not None:
            location_sql, location_params = location.to_sql_params()
            conditions.append(text(location_sql))
            query_params |= location_params

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.session.execute(query, query_params)
        return [model.to_domain() for model in result.scalars().unique().all()]
