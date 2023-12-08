from uuid import UUID

from fastapi import HTTPException, status

from api.v1.users import schemas
from repository.database import AbstractRepository
from repository.exceptions import UserDoesNotExist, UserAlreadyExists
from repository.schemas import UserSchema, UserLoginSchema, Roles
from repository.sql_alchemy import SQLAlchemyRepository
from services.security import SecurityService, get_security_service


class UserService:
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository: AbstractRepository = repository

    async def get(self, *, id: UUID = None, email: str = None) -> UserSchema:
        try:
            if id is not None:
                return await self.repository.get_user_by_id(id)

            if email is not None:
                return await self.repository.get_user_by_email(email)

        except UserDoesNotExist:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    async def create(
        self,
        schema: schemas.UserCreateIn,
        security_service: SecurityService = get_security_service(),
    ) -> UserSchema:
        user_dict = schema.model_dump()
        user_dict["password"] = security_service.create_hashed_password(user_dict["password"])
        try:
            user = await self.repository.create_user(user_dict)
        except UserAlreadyExists:
            raise HTTPException(status.HTTP_409_CONFLICT, "Email already taken")
        else:
            user = await self.repository.set_user_role(user.id, Roles.USER)
            return user

    async def update(self, id: UUID, schema: schemas.UserUpdateIn) -> UserSchema:
        try:
            return await self.repository.update_user(id, schema.model_dump(exclude_unset=True))
        except UserAlreadyExists:
            raise HTTPException(status.HTTP_409_CONFLICT, "Email already taken")

    async def delete(self, id: UUID) -> None:
        try:
            await self.repository.delete_user_by_id(id)
        except UserAlreadyExists:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    async def create_login_record(self, id: UUID, ip_address: str, user_agent: str) -> UserLoginSchema:
        record = await self.repository.create_user_login_record(id, ip_address, user_agent)
        return record

    async def get_login_records(self, id: UUID, limit: int = 10, offset: int = 0) -> list[UserLoginSchema]:
        records = await self.repository.get_user_login_records(id, limit=limit, offset=offset)
        return records


def get_user_service():
    return UserService(SQLAlchemyRepository())
