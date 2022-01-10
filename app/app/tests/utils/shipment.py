import datetime
import uuid

from sqlalchemy.orm import Session

from app.models.main import Country, Shipment
from app.schemas.shipments import CreateShipmentDBSchema, CreateShipmentSchema
from app.tests.utils.location import create_random_location
from app.tests.utils.utils import random_lower_string
from app.utils.shipment import get_shipment_distance_km


def create_random_shipment(db: Session) -> Shipment:
    country = db.query(Country).first()

    from_location = create_random_location(
        name=random_lower_string(), country_uuid=country.uuid, db=db
    )

    to_location = create_random_location(
        name=random_lower_string(), country_uuid=country.uuid, db=db
    )

    shipment_schema = CreateShipmentSchema(
        sender_user_id=uuid.uuid4(),
        receiver_user_id=uuid.uuid4(),
        shipping_date=datetime.date.today(),
        from_location=from_location.uuid,
        to_location=to_location.uuid,
        status="pending",
    )
    shipment_obj = CreateShipmentDBSchema(
        distance_km=get_shipment_distance_km(shipment_schema, db),
        **shipment_schema.dict(),
    )

    instance = Shipment.create_from_schema(obj_in=shipment_obj, session=db)
    return instance
