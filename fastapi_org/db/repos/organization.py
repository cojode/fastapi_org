from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, exists
from sqlalchemy.orm import joinedload

from fastapi_org.domain.organization import (
    OrganizaitonRepository,
    Organization as DomainOrganization,
    ShapedLocation,
)

from fastapi_org.db.models.organization import Organization
from fastapi_org.db.models.activity import Activity
from fastapi_org.db.models.organization_activity import OrganizationActivity

class SQLAlchemyOrganizationRepository(OrganizaitonRepository):
    """SQLAlchemy implementation of the OrganizationRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _execute_and_wrap(self, stmt) -> list[DomainOrganization]:
        result = await self.session.execute(stmt)
        return [org.to_domain() for org in result.scalars().unique().all()]

    async def get_by_id(
        self, organization_id: int
    ) -> DomainOrganization | None:
        stmt = (
            select(Organization)
            .options(
                joinedload(Organization.building),
                joinedload(Organization.activities),
                joinedload(Organization.phone_numbers),
            )
            .where(Organization.id == organization_id)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def search(
        self,
        organization_name: str | None = None,
        building_id: int | None = None,
        activity_id: int | None = None,
        recursive_activity: bool = False,
        location: ShapedLocation | None = None,
    ) -> list[DomainOrganization]:
        query = select(Organization).options(
            joinedload(Organization.building),
            joinedload(Organization.activities),
            joinedload(Organization.phone_numbers),
        )

        conditions, query_params = [], []

        if organization_name:
            conditions.append(
                Organization.name.ilike(f"%{organization_name}%")
            )

        if building_id is not None:
            conditions.append(Organization.building_id == building_id)

        if activity_id is not None:
            activity_tree = (
                select(Activity.id)
                .where(Activity.id == activity_id)
                .cte("activity_tree", recursive=True)
            )
            activity_tree = activity_tree.union_all(
                select(Activity.id).join(
                    activity_tree, Activity.parent_id == activity_tree.c.id
                )
            )

            activity_filter = (
                exists()
                .where(
                    Organization.id == OrganizationActivity.c.organization_id,
                )
                .where(
                    OrganizationActivity.c.activity_id.in_(
                        select(activity_tree.c.id)
                        if recursive_activity
                        else select(Activity.id).where(
                            Activity.id == activity_id
                        )
                    )
                )
            )

            conditions.append(activity_filter)

        if location is not None:
            location_sql, location_params = location.to_sql_params
            conditions.append(location_sql)
            query_params.extend(location_params)

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.session.execute(query, query_params)
        return [model.to_domain() for model in result.scalars().unique().all()]
