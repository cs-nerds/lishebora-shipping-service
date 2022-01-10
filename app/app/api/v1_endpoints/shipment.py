from typing import Any
from uuid import UUID

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.api.deps import get_db
from app.api.utils import ErrorResponseSchema, SuccessResponseSchema
from app.models.main import Shipment
from app.schemas.shipments import (
    CreateShipmentDBSchema,
    CreateShipmentSchema,
    ShipmentInDB,
    UpdateShipmentDBSchema,
    UpdateShipmentSchema,
)
from app.utils.logging import logger
from app.utils.shipment import get_shipment_distance_km

router = APIRouter()


@router.post(
    "/create",
    summary="Create a new shipment",
    response_model=SuccessResponseSchema[ShipmentInDB],
    status_code=201,
)
def create_shipment(
    shipment: CreateShipmentSchema, db: Session = Depends(get_db)
) -> Any:
    try:
        shipment_obj = CreateShipmentDBSchema(
            distance_km=get_shipment_distance_km(shipment, db), **shipment.dict()
        )
        instance = Shipment.create_from_schema(obj_in=shipment_obj, session=db)
        return SuccessResponseSchema[ShipmentInDB](
            message="Shipment created successfully", result=instance
        )
    except IntegrityError:
        logger.exception("IntegrityError: Error creating shipment")
        res = ErrorResponseSchema(error="IntegrityError: Error creating shipment")
        return JSONResponse(jsonable_encoder(res), status_code=400)
    except NoResultFound as e:
        logger.exception(f"NoResultFound: {e}")
        res = ErrorResponseSchema(error=f"NoResultFound: Error creating shipment: {e}")
        return JSONResponse(jsonable_encoder(res), status_code=400)


@router.patch(
    "/update",
    summary="Update a shipment",
    response_model=SuccessResponseSchema[ShipmentInDB],
    status_code=200,
)
def update_shipment(
    shipment: UpdateShipmentSchema, db: Session = Depends(get_db)
) -> Any:
    try:
        shipment_obj = UpdateShipmentDBSchema(
            distance_km=get_shipment_distance_km(shipment, db), **shipment.dict()
        )
        instance = (
            db.query(Shipment).filter(Shipment.uuid == shipment_obj.uuid).scalar()
        )
        if not instance:
            raise NoResultFound
        instance.update_from_schema(updates_in=shipment_obj, session=db)
        return SuccessResponseSchema[ShipmentInDB](
            message="Shipment updated successfully", result=instance
        )
    except IntegrityError:
        logger.exception("IntegrityError: Error updating shipment")
        res = ErrorResponseSchema(error="IntegrityError: Error updating shipment")
        return JSONResponse(jsonable_encoder(res), status_code=400)
    except NoResultFound:
        logger.error(shipment.uuid)
        logger.error("NoResultFound: Error updating shipment, no shipment with that id")
        res = ErrorResponseSchema(error="No shipment found with that id")
        return JSONResponse(jsonable_encoder(res), status_code=404)


@router.get(
    "/details",
    summary="Get a specific shipment details",
    response_model=SuccessResponseSchema[ShipmentInDB],
    status_code=200,
    responses={404: {"model": ErrorResponseSchema}},
)
def get_shipment_details(shipment_uuid: UUID, db: Session = Depends(get_db)) -> Any:
    try:
        instance = db.query(Shipment).filter(Shipment.uuid == shipment_uuid).scalar()
        if not instance:
            raise NoResultFound
        return SuccessResponseSchema[ShipmentInDB](
            message="Shipment retrieved successfully", result=instance
        )
    except NoResultFound:
        logger.error(shipment_uuid)
        logger.error("NoResultFound: Error getting shipment, no shipment with that id")
        res = ErrorResponseSchema(error="No shipment found with that id")
        return JSONResponse(jsonable_encoder(res), status_code=404)
