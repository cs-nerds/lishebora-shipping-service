from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.main import Shipment
from app.schemas.shipments import (CreateShipmentSchema, GetShipmentSchema,
                                   UpdateShipmentSchema)

router = APIRouter()


@router.post("/create", summary="Create a new shipment")
def create_shipment(shipment: CreateShipmentSchema, db: Session = Depends(get_db)):
    instance = Shipment.create_from_schema(obj_in=shipment, session=db,)
    return GetShipmentSchema(**instance.__dict__)


@router.patch("/update", summary="Update a shipment")
def update_shipment(shipment: UpdateShipmentSchema, db: Session = Depends(get_db)):
    instance = db.query(Shipment).filter(Shipment.uuid == shipment.uuid).first()
    instance.update_from_schema(updates_in=shipment, session=db)
    return GetShipmentSchema(**instance.__dict__)


@router.get(
    "/details",
    summary="Get a specific shipment details",
    response_model=GetShipmentSchema,
)
def get_shipment_details(shipment_uuid: UUID, db: Session = Depends(get_db)):
    instance = db.query(Shipment).filter(Shipment.uuid == shipment_uuid).first()
    return GetShipmentSchema(**instance.__dict__)
