from typing import Any

from sqlalchemy.orm import Session

from app.models.main import Country
from app.schemas.countries import CreateCountrySchema, UpdateCountrySchema
from app.tests.utils.country import create_random_country
from app.tests.utils.utils import random_code, random_currency, random_lower_string


def test_create_country_ok(db: Session) -> Any:

    country_schema = CreateCountrySchema(
        name=random_lower_string(), code=random_code(), currency=random_currency()
    )

    instance = Country.create_from_schema(obj_in=country_schema, session=db)

    instance_in_db = db.query(Country).filter(Country.uuid == instance.uuid).scalar()

    assert instance_in_db is not None
    assert instance_in_db == instance

    assert str(instance.code) == country_schema.code
    assert instance.name == country_schema.name
    assert instance.currency == country_schema.currency


def test_update_country_ok(db: Session) -> Any:

    instance = create_random_country(db=db)

    country_schema = UpdateCountrySchema(
        name=random_lower_string(),
        code=random_code(),
        currency=random_currency(),
        uuid=instance.uuid,
    )

    instance.update_from_schema(updates_in=country_schema, session=db)

    assert str(instance.code) == country_schema.code
    assert instance.name == country_schema.name
    assert instance.currency == country_schema.currency
