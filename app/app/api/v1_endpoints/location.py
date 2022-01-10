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
from app.models.main import Location
from app.schemas.locations import CreateLocationSchema, LocationInDB

router = APIRouter()


@router.post(
    "/create",
    summary="Create a new location",
    response_model=SuccessResponseSchema[LocationInDB],
    status_code=201,
)
def create_location(
    location: CreateLocationSchema, db: Session = Depends(get_db)
) -> Any:
    instance = Location.create_from_schema(obj_in=location, session=db)
    return SuccessResponseSchema[LocationInDB](
        message="Location created successfully", result=instance,
    )


@router.get(
    "/list",
    summary="Get a list of available locations",
    response_model=SuccessResponseListSchema[List[LocationInDB]],
    status_code=200,
)
def list_locations(
    country_uuid: UUID,
    list_params: dict = Depends(common_list_params),
    db: Session = Depends(get_db),
) -> Any:
    limit = list_params.get("limit")
    skip = list_params.get("skip")
    instances = (
        db.query(Location)
        .filter(
            Location.country_uuid == country_uuid,
            Location.name.contains(list_params.get("q")),
        )
        .limit(limit=limit)
        .offset(skip)
        .all()
    )

    response = SuccessResponseListSchema[List[LocationInDB]](
        message="Location list retrieved successfully",
        limit=limit,
        skip=skip,
        result=instances,
    ).dict(exclude_none=True)
    return response


@router.get(
    "/details",
    summary="Get details of a specific location",
    response_model=SuccessResponseSchema[LocationInDB],
    status_code=200,
    responses={404: {"model": ErrorResponseSchema}},
)
def get_location_details(location_uuid: UUID, db: Session = Depends(get_db)) -> Any:
    instance = db.query(Location).filter(Location.uuid == location_uuid).first()
    if instance:
        response = SuccessResponseSchema[LocationInDB](
            message="Location details retrieved successfully", result=instance
        ).dict(exclude_none=True)
        return response
    else:
        response = jsonable_encoder(
            ErrorResponseSchema(error="Location does not exist")
        )
        return JSONResponse(content=response, status_code=404)
