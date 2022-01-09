from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.core.conf import settings
from app.models.main import Location
from app.schemas.shipments import CreateShipmentSchema
from app.utils.geopy import get_distance_km as geopy_get_distance_km
from app.utils.mapbox import mapbox_get_distance_km


def get_location_cordinates(
    from_location: UUID, to_location: UUID, db: Session
) -> tuple:

    location_from = db.query(Location).filter(Location.uuid == from_location).first()
    location_to = db.query(Location).filter(Location.uuid == to_location).first()

    if not location_from:
        raise NoResultFound("From location not found")
    if not location_to:
        raise NoResultFound("To location not found")

    return (
        (location_from.latitude, location_from.longitude),
        (location_to.latitude, location_to.longitude),
    )


def get_shipment_distance_km(shipment: CreateShipmentSchema, db: Session) -> float:
    point1, point2 = get_location_cordinates(
        from_location=shipment.from_location, to_location=shipment.to_location, db=db
    )

    distance_between_km = (
        geopy_get_distance_km(point1, point2)
        if settings.DEBUG == "true"
        else mapbox_get_distance_km(point1, point2)
    )

    return round(distance_between_km, 2)
