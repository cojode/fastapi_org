from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from fastapi_org.db.base import Base
from fastapi_org.db.models.organization_activity import OrganizationActivity


class Activity(Base):
    """Activity model."""

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)

    parent = relationship("Activity", remote_side=[id], back_populates="children")
    children = relationship("Activity", back_populates="parent")

    organizations = relationship(
        "Organization",
        secondary=OrganizationActivity,
        back_populates="activities",
    )
