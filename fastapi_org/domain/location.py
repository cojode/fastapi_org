import math
from enum import Enum
from dataclasses import dataclass

from typing import Protocol, Any


class LocationShape(str, Enum):
    CIRCLE = "circle"
    RECTANGULAR = "rect"


class ShapedLocation(Protocol):
    @property
    def to_sql_params(self) -> tuple[str, dict[str, Any]]: ...


@dataclass(frozen=True)
class CircleLocation(ShapedLocation):
    center_la: float
    center_lo: float
    radius: float

    @property
    def to_sql_params(self) -> tuple[str, dict[str, Any]]:
        lat_margin = self.radius / 111.0
        lon_margin = self.radius / (
            111.0 * math.cos(math.radians(self.center_la))
        )

        sql = """
            (b.latitude BETWEEN :min_lat AND :max_lat)
            AND (b.longitude BETWEEN :min_lon AND :max_lon)
            AND (
                POW((b.latitude - :center_la) * 111.0, 2) +
                POW((b.longitude - :center_lo) * 111.0 * COS(RADIANS(:center_la)), 2)
            ) <= POW(:radius, 2)
        """

        params = {
            "min_lat": self.center_la - lat_margin,
            "max_lat": self.center_la + lat_margin,
            "min_lon": self.center_lo - lon_margin,
            "max_lon": self.center_lo + lon_margin,
            "center_la": self.center_la,
            "center_lo": self.center_lo,
            "radius": self.radius,
        }

        return sql, params


@dataclass(frozen=True)
class RectLocation(ShapedLocation):
    first_la: float
    first_lo: float
    second_la: float
    second_lo: float

    @property
    def to_sql_params(self) -> tuple[str, dict[str, Any]]:
        min_la = min(self.first_la, self.second_la)
        max_la = max(self.first_la, self.second_la)
        min_lo = min(self.first_lo, self.second_lo)
        max_lo = max(self.first_lo, self.second_lo)

        sql = """
            (b.latitude BETWEEN :min_lat AND :max_lat)
            AND (b.longitude BETWEEN :min_lon AND :max_lon)
        """

        params = {
            "min_lat": min_la,
            "max_lat": max_la,
            "min_lon": min_lo,
            "max_lon": max_lo,
        }

        return sql, params


SupportedShapedLocations = CircleLocation | RectLocation
