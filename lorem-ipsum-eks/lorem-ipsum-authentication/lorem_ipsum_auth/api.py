from __future__ import annotations
from pydantic import BaseModel, constr, EmailStr
from typing import List, Optional


class Permission(BaseModel):
    name: constr(max_length=100)
    id: constr(max_length=100)

    class Config:
        orm_mode = True


class Role(BaseModel):
    id: Optional[int]
    name: constr(max_length=100)
    default: Optional[bool] = False
    permissions: List[Permission]

    class Config:
        orm_mode = True


class User(BaseModel):
    id: Optional[int]
    username: constr(max_length=100)
    email: EmailStr
    login_type: constr(max_length=100)
    role: Role

    class Config:
        orm_mode = True
