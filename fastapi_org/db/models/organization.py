from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_org.db.base import Base
from fastapi_org.db.models.organization_activity import OrganizationActivity
from fastapi_org.domain.organization import Organization as DomainOrganization


class Organization(Base):
    """Organization model."""

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")

    activities = relationship(
        "Activity",
        secondary=OrganizationActivity,
        back_populates="organizations",
    )

    phone_numbers = relationship("PhoneNumber", back_populates="organization")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
        }

    def to_domain(self) -> DomainOrganization:
        return DomainOrganization(
            id=self.id,
            name=self.name,
            building_id=self.building_id,
            building=self.building.to_dict(),
            activities=[
                {"id": a.id, "name": a.name, "parent_id": a.parent_id}
                for a in self.activities
            ],
            phone_numbers=[p.phone_number for p in self.phone_numbers],
        )
