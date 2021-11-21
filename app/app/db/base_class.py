from typing import Any

from pydantic import BaseModel as BaseSchema
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm.session import Session


@as_declarative()
class Base:
    id: Any
    __name__: str

    def __init__(self, **kwargs: Any) -> None:
        raise NotImplementedError

    @classmethod
    def create_from_schema(cls, obj_in: BaseSchema, session: Session) -> Any:
        obj = cls(**obj_in.dict())
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def update_from_schema(self, updates_in: BaseSchema, session: Session) -> Any:
        update_data = updates_in.dict(exclude_unset=True)
        for key in update_data.keys():
            setattr(self, key, update_data.get(key))
        session.commit()
        session.refresh(self)
        return self
