from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class LocationShape(str, Enum):
    """Location shape specifier."""

    SQUARE = "square"
    CIRCLE = "circle"


@dataclass
class LocationCondition:
    """Location describer."""

    center_latitude: float
    center_longitude: float
    radius: float
    shape: LocationShape


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
    async def filter_by_building_id(self, building_id: int) -> list[Organization]:
        """A list of all organizations located in a specific building."""

    @abstractmethod
    async def filter_by_exact_activity_id(self, activity_id: int) -> list[Organization]:
        """A list of all organizations that belong to a specified type of activity."""

    @abstractmethod
    async def filter_by_related_activity_id(
        self,
        activity_id: int,
    ) -> list[Organization]:
        """A list of all organizations that are related to a specified activity."""

    @abstractmethod
    async def filter_by_location(
        self,
        condition: LocationCondition,
    ) -> list[Organization]:
        """A list of organizations that are within a specified area."""

    @abstractmethod
    async def get_by_id(self, organization_id: int) -> Organization | None:
        """Displaying information about an organization by its ID."""

    @abstractmethod
    async def get_by_name(self, organization_name: int) -> Organization | None:
        """Searching for an organization by name."""
