from sqlalchemy.orm import Session

from app.models.main import Country
from app.schemas.countries import CreateCountrySchema
from app.core.conf import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    country = db.query(Country).filter(Country.name == "Kenya").scalar()
    if not country:
        country_in = CreateCountrySchema(
            name="Kenya",
            code="254",
            currency="KES"
        )
        Country.create_from_schema(obj_in=country_in, session=db)  # noqa: F841