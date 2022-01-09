from typing import Any

from sqlalchemy.orm import Session

from app.models.main import Country, Location
from app.schemas.locations import UpdateLocationSchema
from app.tests.utils.location import create_random_location
from app.tests.utils.utils import random_lower_string


def test_create_location_ok(db: Session) -> Any:
    location_name = random_lower_string()
    country = db.query(Country).first()

    instance = create_random_location(
        name=location_name, country_uuid=country.uuid, db=db
    )

    assert type(instance) == Location
    assert instance.country_uuid == country.uuid
    assert instance.name == location_name
    assert instance.latitude is not None
    assert instance.longitude is not None


def test_update_location_ok(db: Session) -> Any:
    location_name = random_lower_string()
    country = db.query(Country).first()

    instance = create_random_location(
        name=location_name, country_uuid=country.uuid, db=db
    )

    location_schema = UpdateLocationSchema(
        name=random_lower_string(),
        uuid=instance.uuid,
    )

    instance.update_from_schema(updates_in=location_schema, session=db)

    assert type(instance) == Location
    assert instance.country_uuid == country.uuid
    assert instance.name == location_schema.name
