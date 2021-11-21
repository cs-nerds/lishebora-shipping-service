from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


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


class UpdateShipmentSchema(BaseShipmentSchema):
    uuid: UUID


class GetShipmentSchema(BaseShipmentSchema):
    uuid: UUID
    distance_km: Optional[float] = None
    total_cost: Optional[float] = None
