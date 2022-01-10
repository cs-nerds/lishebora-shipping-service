from sqlalchemy.orm import Session

from app.models.main import Country
from app.schemas.countries import CreateCountrySchema
from app.tests.utils.utils import random_code, random_currency, random_lower_string


def create_random_country(db: Session) -> Country:
    country = CreateCountrySchema(
        name=random_lower_string(), code=random_code(), currency=random_currency()
    )
    instance = Country.create_from_schema(obj_in=country, session=db)
    return instance
