from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, root_validator


class ShipmentStatusTypes(str, Enum):
    pending = "pending"
    intransit = "intransit"
    delivered = "delivered"
    cancelled = "cancelled"


class BaseShipmentSchema(BaseModel):
    from_location: Optional[UUID] = None
    to_location: Optional[UUID] = None
    product_weight: Optional[float] = None
    product_volume: Optional[float] = None
    shipping_date: Optional[date] = None
    sender_user_id: Optional[UUID] = None
    receiver_user_id: Optional[UUID] = None
    status: ShipmentStatusTypes


class CreateShipmentSchema(BaseShipmentSchema):
    sender_user_id: UUID
    receiver_user_id: UUID
    shipping_date: date
    from_location: UUID
    to_location: UUID


class CreateShipmentDBSchema(CreateShipmentSchema):
    distance_km: float
    total_cost: Optional[float] = 0.0

    @root_validator(pre=False)
    def _set_fields(cls, values: dict) -> dict:
        """This is a validator that sets the field values based on the
        the shipment distance in km.

        Args:
            values (dict): Stores the attributes of the CreateShipmentDBSchema object.

        Returns:
            dict: The attributes of the shipment object with the shipment's fields.
        """
        values["total_cost"] = round((values["distance_km"] * 25.0), 2)
        return values


class UpdateShipmentSchema(CreateShipmentSchema):
    uuid: UUID


class UpdateShipmentDBSchema(CreateShipmentDBSchema):
    uuid: UUID


class GetShipmentSchema(BaseShipmentSchema):
    uuid: UUID
    distance_km: Optional[float] = None
    total_cost: Optional[float] = None


class ShipmentInDB(GetShipmentSchema):
    class Config:
        orm_mode = True
