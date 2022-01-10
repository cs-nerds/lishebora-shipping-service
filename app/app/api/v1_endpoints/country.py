from typing import Any, List
from uuid import UUID

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.utils import (
    ErrorResponseSchema,
    SuccessResponseListSchema,
    SuccessResponseSchema,
    common_list_params,
)
from app.models.main import Country
from app.schemas.countries import CountryInDB

router = APIRouter()


@router.get(
    "/list",
    summary="Get a list of all available countries",
    response_model=SuccessResponseListSchema[List[CountryInDB]],
    status_code=200,
)
def list_countries(
    list_params: dict = Depends(common_list_params), db: Session = Depends(get_db)
) -> Any:
    limit = list_params.get("limit")
    skip = list_params.get("skip")
    instances = db.query(Country).limit(limit=limit).offset(skip).all()
    response = SuccessResponseListSchema[List[CountryInDB]](
        message="Country list retrieved successfully",
        result=instances,
        limit=limit,
        skip=skip,
    ).dict(exclude_none=True)

    return response


@router.get(
    "/details",
    summary="Get a specific country details",
    response_model=SuccessResponseSchema[CountryInDB],
    status_code=200,
    responses={404: {"model": ErrorResponseSchema}},
)
def get_country_details(country_uuid: UUID, db: Session = Depends(get_db)) -> Any:
    instance = db.query(Country).filter(Country.uuid == country_uuid).first()
    if instance:
        return SuccessResponseSchema[CountryInDB](
            message="Country details retrieved successfully", result=instance.__dict__
        ).dict(exclude_none=True)
    else:
        response = jsonable_encoder(ErrorResponseSchema(error="Country does not exist"))
        return JSONResponse(content=response, status_code=404)
