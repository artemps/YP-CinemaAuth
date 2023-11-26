import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field


class UserLoginIn(BaseModel):
    login: str = Field(..., max_length=255, description="Account login information")
    password: str = Field(..., max_length=255, description="Account password")


class UserLoginOut(BaseModel):
    access_token: str = Field(..., description="Access token for authentication")
    token_type: str = Field(..., description="Token type for authentication")


class UserRegisterIn(BaseModel):
    login: str = Field(..., max_length=255, description="Account login information")
    password: str = Field(..., max_length=255, min_value=8, description="Account password")
    first_name: str = Field(None, max_length=50, description="Account first name")
    last_name: str = Field(None, max_length=50, description="Account last name")


class UserRegisterOut(BaseModel):
    id: UUID = Field(..., description="Unique user identifier")
    first_name: str = Field(None, description="Account first name")
    last_name: str = Field(None, description="Account last name")
    created_at: dt.datetime = Field(..., description="Account creation date")

