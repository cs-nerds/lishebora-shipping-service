from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class ResponseBaseSchema(BaseModel):
    status: str
    message: Optional[str]
    result: Optional[Union[str, List[Dict[str, Any]], Dict[str, Any]]]
    error: Optional[str]
    skip: Optional[int]
    limit: Optional[int]


class SuccessResponseSchema(BaseModel):
    status: str = "success"
    message: str
    result: Dict[str, Any]


class SuccessResponseListSchema(BaseModel):
    status: str = "success"
    message: str
    result: List[Any]


class ErrorResponseSchema(BaseModel):
    status: str = "error"
    error: str


def common_list_params(limit: int=10, skip: int=0, q: str=""):
    return {"limit": limit, "skip": skip, "q": q}
