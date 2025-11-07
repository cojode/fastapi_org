from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from fastapi_org.db.base import Base


class Building(Base):
    """Building model."""

    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(255), nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")
