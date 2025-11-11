from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fastapi_org.db.base import Base


class PhoneNumber(Base):
    """PhoneNumber model."""

    __tablename__ = "phone_numbers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
    )

    organization = relationship("Organization", back_populates="phone_numbers")
