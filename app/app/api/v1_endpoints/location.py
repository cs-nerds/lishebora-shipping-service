from typing import Any
from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.models.main import Location
from app.schemas.locations import CreateLocationSchema, GetLocationSchema
from app.api.utils import common_list_params, SuccessResponseSchema, SuccessResponseListSchema, ErrorResponseSchema
from typing import List

from app.api.deps import get_db

router = APIRouter()


@router.post("/create", summary="Create a new location", response_model=GetLocationSchema)
def create_location(location: CreateLocationSchema, db: Session = Depends(get_db)) -> Any:
    instance = Location.create_from_schema(
        obj_in=location,
        session=db
    )
    return GetLocationSchema(**instance.__dict__)


@router.get("/list", summary="Get a list of available locations", response_model=SuccessResponseSchema)
def list_locations(list_params: dict = Depends(common_list_params), db: Session = Depends(get_db)) -> Any:
    instances = db.query(Location).limit(limit=list_params.get("limit")).offset(list_params.get("skip")).all()
    response = SuccessResponseListSchema(
        message="Location list retrieved successfully",
        result=instances
    ).dict(exclude_none=True)
    return response


@router.get("/details", summary="Get details of a specific location", response_model=GetLocationSchema)
def get_location_details(location_uuid: UUID, db: Session = Depends(get_db)) -> Any:
    instance = db.query(Location).filter(Location.uuid == location_uuid).first()
    if instance:
        response = SuccessResponseSchema(
            message="Location details retrieved successfully",
            result=instance.__dict__
        ).dict(exclude_none=True)
        return response
    else:
        response = jsonable_encoder(ErrorResponseSchema(
            error="Location does not exist"
        ))
        return JSONResponse(content=response, status_code=404)
