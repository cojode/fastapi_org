from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


class LocationShape(str, Enum):
    CIRCLE = "circle"
    RECTANGULAR = "rect"


class ShapedLocation(Protocol):

    def to_sql_params(
        self,
        building_table_alias: str = "buildings",
    ) -> tuple[str, dict[str, Any]]: ...


@dataclass(frozen=True)
class CircleLocation(ShapedLocation):
    center_la: float
    center_lo: float
    radius: float

    def to_sql_params(
        self,
        building_table_alias: str = "buildings",
    ) -> tuple[str, dict[str, Any]]:
        sql = f"""
            (6371000 * 2 * ASIN(
            SQRT(
            POW(SIN(RADIANS({building_table_alias}.latitude - :center_la) / 2), 2) +
            COS(RADIANS(:center_la)) * COS(RADIANS({building_table_alias}.latitude)) *
            POW(SIN(RADIANS({building_table_alias}.longitude - :center_lo) / 2), 2)
            )
            )) <= :radius
        """

        params = {
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

    def to_sql_params(
        self,
        building_table_alias: str = "buildings",
    ) -> tuple[str, dict[str, Any]]:
        min_la = min(self.first_la, self.second_la)
        max_la = max(self.first_la, self.second_la)
        min_lo = min(self.first_lo, self.second_lo)
        max_lo = max(self.first_lo, self.second_lo)

        sql = f"""
            ({building_table_alias}.latitude BETWEEN :min_lat AND :max_lat)
            AND ({building_table_alias}.longitude BETWEEN :min_lon AND :max_lon)
        """

        params = {
            "min_lat": min_la,
            "max_lat": max_la,
            "min_lon": min_lo,
            "max_lon": max_lo,
        }

        return sql, params


SupportedShapedLocations = CircleLocation | RectLocation
