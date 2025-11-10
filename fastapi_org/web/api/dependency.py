from fastapi import Query

from fastapi_org.domain.location import LocationShape


class LocationParams:

    def __init__(
        self,
        location_shape: LocationShape | None = Query(
            None,
            description="Type of search area: 'circle' or 'rectangular'",
        ),
        center_la: float | None = Query(
            None,
            ge=-90,
            le=90,
            description="Latitude of circle center (degrees, -90 to 90)",
        ),
        center_lo: float | None = Query(
            None,
            ge=-180,
            le=180,
            description="Longitude of circle center (degrees, -180 to 180)",
        ),
        radius: float | None = Query(
            None,
            gt=0,
            description="Radius for circular search in meters (must be > 0)",
        ),
        first_la: float | None = Query(
            None,
            ge=-90,
            le=90,
            description="First latitude corner of rectangle (degrees, -90 to 90)",
        ),
        first_lo: float | None = Query(
            None,
            ge=-180,
            le=180,
            description="First longitude corner of rectangle (degrees, -180 to 180)",
        ),
        second_la: float | None = Query(
            None,
            ge=-90,
            le=90,
            description="Second latitude corner of rectangle (degrees, -90 to 90)",
        ),
        second_lo: float | None = Query(
            None,
            ge=-180,
            le=180,
            description="Second longitude corner of rectangle (degrees, -180 to 180)",
        ),
    ):
        self.location_shape = location_shape
        self.center_la = center_la
        self.center_lo = center_lo
        self.radius = radius
        self.first_la = first_la
        self.first_lo = first_lo
        self.second_la = second_la
        self.second_lo = second_lo
