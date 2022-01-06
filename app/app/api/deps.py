from typing import Any, Generator

from mapbox import Geocoder

from app.api.utils import (ErrorResponseSchema, SuccessResponseListSchema,
                           SuccessResponseSchema)
from app.db.session import SessionLocal


def get_db() -> Generator:

    try:
        db = SessionLocal()
        yield db

    finally:
        db.close()


def get_list_res() -> dict:
    return {
        200: {"model": SuccessResponseListSchema},
        404: {"model": ErrorResponseSchema},
    }


def get_res() -> dict:
    return {
        201: {"model": SuccessResponseSchema},
        200: {"model": SuccessResponseSchema},
        404: {"model": ErrorResponseSchema},
    }


def mapbox_geocoding(
    location_name: str, country: str = "Ke", language: str = "en"
) -> Any:
    geocoder = Geocoder()
    response = geocoder.forward(
        address=location_name, country=country, languages=language
    )
    return response
