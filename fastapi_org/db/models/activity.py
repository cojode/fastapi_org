from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_org.db.base import Base
from fastapi_org.db.models.organization_activity import OrganizationActivity


class Activity(Base):
    """Activity model."""

    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id"),
        nullable=True,
    )

    parent = relationship("Activity", remote_side=[id], back_populates="children")
    children = relationship("Activity", back_populates="parent")

    organizations = relationship(
        "Organization",
        secondary=OrganizationActivity,
        back_populates="activities",
    )
