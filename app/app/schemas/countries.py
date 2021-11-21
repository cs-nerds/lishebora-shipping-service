from typing import Optional
from uuid import UUID
from typing import List
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
