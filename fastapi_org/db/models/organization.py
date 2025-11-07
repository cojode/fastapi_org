from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from fastapi_org.db.base import Base
from fastapi_org.db.models.organization_activity import OrganizationActivity


class Organization(Base):
    """Organization model."""

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")

    activities = relationship(
        "Activity",
        secondary=OrganizationActivity,
        back_populates="organizations",
    )

    phone_numbers = relationship("PhoneNumber", back_populates="organization")
