from __future__ import annotations
from pydantic import BaseModel, constr
from typing import List, Optional


class Permission(BaseModel):
    name: constr(max_length=100)
    id: constr(max_length=100)

    class Config:
        orm_mode = True


class Role(BaseModel):
    id: Optional[int]
    name: constr(max_length=100)
    default: bool
    permissions: List[Permission]

    class Config:
        orm_mode = True
