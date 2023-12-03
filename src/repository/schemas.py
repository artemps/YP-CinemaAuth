import datetime as dt
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field, validator


class Roles(StrEnum):
    USER = "USR"
    MANAGER = "MNG"
    SUPERVISOR = "SVR"
    ANALYST = "ANA"
    TESTER = "TST"
    EXECUTOR = "EXC"
    ADMIN = "ADM"


class UserRoleSchema(BaseModel):
    id: UUID
    name: Roles

    class Config:
        orm_mode = True


class BaseUserSchema(BaseModel):
    id: UUID
    login: str
    password: str
    first_name: str
    last_name: str
    created_at: dt.datetime

    class Config:
        orm_mode = True


class UserSchema(BaseUserSchema):
    roles: list[UserRoleSchema]


class UserLoginSchema(BaseModel):
    id: UUID
    user_id: UUID
    login_at: dt.datetime
    ip_address: str
    user_agent: str

    class Config:
        orm_mode = True
