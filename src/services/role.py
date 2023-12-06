from uuid import UUID

from fastapi import HTTPException, status

from repository.database import AbstractRepository
from repository.exceptions import RoleDoesNotExist, RoleAlreadyExists, UserAlreadyExists, UserDoesNotExist
from repository.schemas import UserSchema, Roles
from repository.sql_alchemy import SQLAlchemyRepository


class RoleService:
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository: AbstractRepository = repository

    async def set(self, user_id: UUID, role: Roles) -> UserSchema:
        try:
            return await self.repository.set_user_role(user_id, role)
        except UserDoesNotExist:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        except RoleAlreadyExists:
            raise HTTPException(status.HTTP_409_CONFLICT, f"User already has role {role}")

    async def remove(self, user_id: UUID, role: Roles) -> UserSchema:
        try:
            return await self.repository.remove_user_role(user_id, role)
        except UserDoesNotExist:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        except RoleDoesNotExist:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"User does not have role {role}")


def get_role_service():
    return RoleService(SQLAlchemyRepository())
