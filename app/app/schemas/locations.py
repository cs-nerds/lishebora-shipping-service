from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseLocationSchema(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    country_uuid: Optional[UUID] = None


class CreateLocationSchema(BaseLocationSchema):
    name: str
    latitude: float
    longitude: float
    country_uuid: UUID


class UpdateLocationSchema(BaseLocationSchema):
    uuid: UUID


class GetLocationSchema(BaseLocationSchema):
    uuid: UUID
