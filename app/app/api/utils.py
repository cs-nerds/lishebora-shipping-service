from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

DataType = TypeVar("DataType")


class ResponseStatusTypes(str, Enum):
    success = "success"
    error = "error"


class ResponseWrapperBaseSchema(GenericModel, Generic[DataType]):
    status: ResponseStatusTypes
    message: Optional[str] = None
    limit: Optional[int] = None
    skip: Optional[int] = None
    result: Optional[DataType] = None
    error: Optional[str]


class SuccessResponseListSchema(GenericModel, Generic[DataType]):
    status: Optional[str] = ResponseStatusTypes.success.name
    message: str
    limit: Optional[int] = None
    skip: Optional[int] = None
    result: Optional[DataType] = None


class SuccessResponseSchema(GenericModel, Generic[DataType]):
    status: Optional[str] = ResponseStatusTypes.success.name
    message: str
    result: Optional[DataType] = None


class ErrorResponseSchema(BaseModel):
    status: Optional[str] = ResponseStatusTypes.error.name
    error: str


def common_list_params(limit: int = 10, skip: int = 0, q: str = "") -> dict:
    return {"limit": limit, "skip": skip, "q": q}
