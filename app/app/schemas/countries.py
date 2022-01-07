from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class BaseCountrySchema(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    currency: Optional[str] = None


class CreateCountrySchema(BaseCountrySchema):
    name: str
    code: str
    currency: str


class UpdateCountrySchema(BaseCountrySchema):
    uuid: UUID


class GetCountrySchema(BaseCountrySchema):
    uuid: UUID


class CountryListSchema(BaseModel):
    __root__: List[GetCountrySchema]


class CountryInDB(BaseCountrySchema):
    uuid: UUID
    class Config:
        orm_mode = True
