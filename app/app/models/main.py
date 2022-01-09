import datetime
import uuid
from typing import Any

from pydantic import BaseModel as BaseSchema
from sqlalchemy import Column, Date, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.db.base_class import Base
from app.schemas.shipments import ShipmentStatusTypes


class Country(Base):
    __tablename__ = "countries"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True, unique=True)
    code = Column(Integer, nullable=True, index=True, unique=True)
    currency = Column(String, default="KES", nullable=True)
    createdat = Column(DateTime, default=datetime.datetime.now)
    updateat = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class Location(Base):
    __tablename__ = "locations"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True)
    longitude = Column(Float)
    latitude = Column(Float)
    country_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("countries.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    createdat = Column(DateTime, default=datetime.datetime.now)
    updatedat = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class FuelCost(Base):
    __tablename__ = "fuel_costs"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    petrol_cost = Column(Float)
    diesel_cost = Column(Float)
    currency = Column(String)
    createdat = Column(DateTime, default=datetime.datetime.now)
    updatedat = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class Shipment(Base):
    __tablename__ = "shipments"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_location = Column(
        UUID(as_uuid=True),
        ForeignKey("locations.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    to_location = Column(
        UUID(as_uuid=True),
        ForeignKey("locations.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    distance_km = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    product_weight = Column(Float, nullable=True)
    product_volume = Column(Float, nullable=True)
    shipping_date = Column(Date, nullable=False)
    sender_user_id = Column(UUID(as_uuid=True), index=True)
    receiver_user_id = Column(UUID(as_uuid=True), index=True)
    status = Column(Enum(ShipmentStatusTypes), nullable=False)
    createdat = Column(DateTime, default=datetime.datetime.now)
    updatedat = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )

    def update_from_schema(self, updates_in: BaseSchema, session: Session) -> Any:
        update_data = updates_in.dict(exclude_none=True)
        for key in update_data.keys():
            setattr(self, key, update_data.get(key))
        session.commit()
        session.refresh(self)
        return self
