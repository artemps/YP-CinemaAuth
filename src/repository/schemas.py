import datetime as dt
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


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


class UserSchema(BaseModel):
    id: UUID
    login: str
    password: str
    roles: list[UserRoleSchema]
    first_name: str
    last_name: str


class UserLoginSchema(BaseModel):
    id: UUID
    user_id: UUID
    login_at: dt.datetime
    ip_address: str
    user_agent: str
