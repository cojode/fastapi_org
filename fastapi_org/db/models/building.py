from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_org.db.base import Base


class Building(Base):
    """Building model."""

    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(nullable=False, unique=True)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    organizations = relationship("Organization", back_populates="building")
