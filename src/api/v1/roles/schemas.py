from pydantic import BaseModel, Extra


class RoleIn(BaseModel):
    name: str

    class Config:
        extra = Extra.forbid
