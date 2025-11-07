from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from fastapi_org.db.base import Base


class PhoneNumber(Base):
    """PhoneNumber model."""

    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(20), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    organization = relationship("Organization", back_populates="phone_numbers")
