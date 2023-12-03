from uuid import UUID

from fastapi import HTTPException, status

from repository.database import AbstractRepository
from repository.exceptions import ObjectDoesNotExist
from repository.schemas import UserSchema, Roles
from repository.sql_alchemy import SQLAlchemyRepository


class RoleService:
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository: AbstractRepository = repository

    async def set(self, *, user_id: UUID, role: Roles) -> UserSchema:
        try:
            return await self.repository.set_user_role(user_id, role)
        except ObjectDoesNotExist:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    async def remove(self, *, user_id: UUID, role: Roles) -> UserSchema:
        try:
            return await self.repository.remove_user_role(user_id, role)
        except ObjectDoesNotExist:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")



def get_role_service():
    return RoleService(SQLAlchemyRepository())
