from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    login: str
    password: str
