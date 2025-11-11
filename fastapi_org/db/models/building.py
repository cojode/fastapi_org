from typing import Any

from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_org.db.base import Base
from fastapi_org.domain.building import Building as DomainBuilding


class Building(Base):
    """Building model."""

    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(nullable=False, unique=True)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    organizations = relationship("Organization", back_populates="building")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    def to_domain(self) -> DomainBuilding:
        return DomainBuilding(
            id=self.id,
            address=self.address,
            latitude=self.latitude,
            longitude=self.longitude,
            organizations=[org.to_dict() for org in self.organizations],
        )
