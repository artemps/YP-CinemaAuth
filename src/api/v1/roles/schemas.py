from pydantic import BaseModel, Extra

from repository.schemas import Roles


class RoleIn(BaseModel):
    name: Roles

    class Config:
        extra = Extra.forbid
