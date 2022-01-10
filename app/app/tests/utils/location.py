from uuid import UUID

from sqlalchemy.orm import Session

from app.models.main import Location
from app.schemas.locations import CreateLocationSchema
from app.tests.utils.utils import random_latitude, random_longitude


def create_random_location(name: str, country_uuid: UUID, db: Session) -> Location:
    location = CreateLocationSchema(
        name=name,
        latitude=random_latitude(),
        longitude=random_longitude(),
        country_uuid=country_uuid,
    )
    instance = Location.create_from_schema(obj_in=location, session=db)
    return instance
