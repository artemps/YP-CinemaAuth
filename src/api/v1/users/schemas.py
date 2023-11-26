import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field


class UserMeOut(BaseModel):
    id: UUID = Field(..., description="Unique user identifier")
    first_name: str = Field(None, description="Account first name")
    last_name: str = Field(None, description="Account last name")
    created_at: dt.datetime = Field(..., description="Account creation date")

