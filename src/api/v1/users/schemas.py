import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Extra, Field, validator, EmailStr


class UserOut(BaseModel):
    id: UUID = Field(..., description="Unique user identifier")
    first_name: str | None = Field(None, description="Account first name")
    last_name: str | None = Field(None, description="Account last name")
    created_at: dt.datetime = Field(..., description="Account creation date")
    roles: list[str] = Field([], description="List of user roles")

    @validator("roles", pre=True)
    def _objects_to_list(cls, v):
        return [role.name for role in v]


class UserUpdateIn(BaseModel):
    first_name: str | None = Field(None, min_length=5, max_length=50, description="Account first name")
    last_name: str | None = Field(None, min_length=5, max_length=50, description="Account last name")

    class Config:
        extra = Extra.forbid


class UserCreateIn(BaseModel):
    email: EmailStr = Field(..., max_length=255, description="Account email information")
    password: str = Field(..., max_length=255, min_length=8, description="Account password")
    first_name: str = Field("", min_length=5, max_length=50, description="Account first name")
    last_name: str = Field("", min_length=5, max_length=50, description="Account last name")

    class Config:
        extra = Extra.forbid


class UserLoginHistoryOut(BaseModel):
    login_at: dt.datetime
    ip_address: str
    user_agent: str

