from pydantic import BaseModel, Extra, Field


class UserLoginIn(BaseModel):
    email: str = Field(..., max_length=255, description="Account email information")
    password: str = Field(..., max_length=255, description="Account password")

    class Config:
        extra = Extra.forbid


class UserLoginOut(BaseModel):
    access_token: str = Field(..., description="Access token for authentication")
    refresh_token: str = Field(..., description="Refresh token for authentication")
    token_type: str = Field(..., description="Token type for authentication")


class UserLogout(BaseModel):
    success: str = Field(True)
