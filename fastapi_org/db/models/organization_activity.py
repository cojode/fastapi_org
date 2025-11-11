from sqlalchemy import Column, ForeignKey, Integer, Table

from fastapi_org.db.base import Base

OrganizationActivity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id")),
    Column("activity_id", Integer, ForeignKey("activities.id")),
)
