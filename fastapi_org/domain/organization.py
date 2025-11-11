from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from fastapi_org.domain.location import ShapedLocation


@dataclass
class Organization:
    """Organization domain."""

    id: int
    name: str
    building_id: int
    building: dict[Any, Any]
    activities: list[Any]
    phone_numbers: list[Any]


class OrganizaitonRepository(ABC):
    """Repository interface for organization model."""

    @abstractmethod
    async def search(
        self,
        organization_name: str | None = None,
        building_id: int | None = None,
        activity_id: int | None = None,
        recursive_activity: bool = False,
        location: ShapedLocation | None = None,
    ) -> list[Organization]:
        """A list of all organizations located in a specific building."""

    @abstractmethod
    async def get_by_id(self, organization_id: int) -> Organization | None:
        """Displaying information about an organization by its ID."""
