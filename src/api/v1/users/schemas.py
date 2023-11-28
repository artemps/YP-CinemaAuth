import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field, Extra


class UserOut(BaseModel):
    id: UUID = Field(..., description="Unique user identifier")
    first_name: str | None = Field(None, description="Account first name")
    last_name: str | None = Field(None, description="Account last name")
    created_at: dt.datetime = Field(..., description="Account creation date")

    class Config:
        orm_mode = True


class UserUpdateIn(BaseModel):
    first_name: str | None = Field(None, min_length=5, max_length=50, description="Account first name")
    last_name: str | None = Field(None, min_length=5, max_length=50, description="Account last name")

    class Config:
        extra = Extra.forbid


class UserCreateIn(BaseModel):
    login: str = Field(..., max_length=255, description="Account login information")
    password: str = Field(..., max_length=255, min_length=8, description="Account password")
    first_name: str = Field(None, min_length=5, max_length=50, description="Account first name")
    last_name: str = Field(None, min_length=5, max_length=50, description="Account last name")

    class Config:
        extra = Extra.forbid
