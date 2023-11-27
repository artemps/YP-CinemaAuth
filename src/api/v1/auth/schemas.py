import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field, Extra


class UserLoginIn(BaseModel):
    login: str = Field(..., max_length=255, description="Account login information")
    password: str = Field(..., max_length=255, description="Account password")

    class Config:
        extra = Extra.forbid


class UserLoginOut(BaseModel):
    access_token: str = Field(..., description="Access token for authentication")
    token_type: str = Field(..., description="Token type for authentication")
