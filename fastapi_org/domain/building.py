from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from fastapi_org.domain.location import ShapedLocation


@dataclass
class Building:
    id: int
    address: str
    latitude: float
    longitude: float

    organizations: list[Any]


class BuildingRepository(ABC):
    """Repository interface for building model."""

    @abstractmethod
    async def search(
        self,
        location: ShapedLocation | None = None,
    ) -> list[Building]:
        """A list of all building with the location filter."""
