from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_org.db.base import Base
from fastapi_org.db.models.organization_activity import OrganizationActivity


class Organization(Base):
    """Organization model."""

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    building_id: Mapped[str] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")

    activities = relationship(
        "Activity",
        secondary=OrganizationActivity,
        back_populates="organizations",
    )

    phone_numbers = relationship("PhoneNumber", back_populates="organization")
