from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from api.v1.users import schemas
from models import User
from repository.database import AbstractRepository, UserRepository
from services.security import SecurityService


class UserService:
    def __init__(self, repository: AbstractRepository) -> None:
        self.repository: AbstractRepository = repository

    async def create(
        self,
        user_create: schemas.UserCreateIn,
        security_service: SecurityService,
    ) -> User:
        exists = await self.repository.check_unique_login(user_create.login)
        if exists:
            raise HTTPException(status.HTTP_409_CONFLICT, "Login already taken")

        user_dict = user_create.model_dump()
        user_dict["password"] = security_service.create_hashed_password(user_dict["password"])
        await self.repository.add_one(user_dict)
        user = await self.repository.get_by_login(user_dict["login"])
        return user

    async def update(self, id: UUID, schema: schemas.UserUpdateIn) -> User:
        await self.repository.update_one(id, schema.model_dump(exclude_unset=True))
        user = await self.get(id=id)
        return user

    async def get(self, *, id: UUID = None, login: str = None) -> User:
        try:
            if id is not None:
                return await self.repository.get_by_id(id)

            if login is not None:
                return await self.repository.get_by_login(login)

        except NoResultFound:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

        except MultipleResultsFound:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Multiple users found")

    async def make_login(self, user: User) -> None:
        await self.repository.make_login(user)


def get_user_service():
    return UserService(UserRepository())
