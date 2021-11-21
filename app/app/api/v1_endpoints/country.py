from typing import Any
from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.schemas.countries import GetCountrySchema, CountryListSchema
from app.api.utils import SuccessResponseListSchema, common_list_params, SuccessResponseSchema, ErrorResponseSchema
from typing import List
from app.models.main import Country

from app.api.deps import get_db

router = APIRouter()


@router.get(
    "/list", summary="Get a list of all available countries",
    response_model=SuccessResponseListSchema
)
def list_countries(list_params: dict = Depends(common_list_params), db: Session = Depends(get_db)) -> Any:
    instances = db.query(Country).limit(limit=list_params.get("limit")).offset(list_params.get("skip")).all()
    response = SuccessResponseListSchema(
        status="success",
        message="Country list retrieved successfully",
        result=instances
    ).dict(exclude_none=True)

    return response


@router.get(
    "/details", summary="Get a specific country details",
    response_model=SuccessResponseSchema
)
def get_country_details(country_uuid: UUID, db: Session = Depends(get_db)) -> Any:
    instance = db.query(Country).filter(Country.uuid == country_uuid).first()
    if instance:
        return SuccessResponseSchema(
            message="Country details retrieved successfully",
            result=instance.__dict__
        ).dict(exclude_none=True)
    else:
        response = jsonable_encoder(ErrorResponseSchema(
            error="Country does not exist"
        ))
        return JSONResponse(content=response, status_code=404)
