from sqlalchemy.orm import DeclarativeBase

from fastapi_org.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
