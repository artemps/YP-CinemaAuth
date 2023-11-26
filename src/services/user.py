from uuid import UUID

from werkzeug.security import check_password_hash, generate_password_hash

from repository.database import AbstractRepository, UserRepository
from schemas import UserCreate, UserLogin


class UserService:
    def __init__(self, repository: AbstractRepository):
        self.repository: AbstractRepository = repository

    async def add_user(self, user_create: UserCreate) -> str:
        exists = await self.repository.check_unique_login(user_create.login)
        if exists:
            return "Login exists"
        user_dict = user_create.model_dump()
        user_dict["password"] = generate_password_hash(user_dict["password"])
        await self.repository.add_one(user_dict)
        return "Created"

    async def edit_user(self, user_id: UUID, user_update: UserCreate) -> str:
        exists = await self.repository.check_unique_login(user_update.login)
        if exists:
            return "Login exists"
        user_dict = user_update.model_dump()
        await self.repository.update_one(user_id, user_dict)
        return "Updated"

    async def make_login(self, credentials: UserLogin) -> str:
        user = await self.repository.get_by_login(credentials.login)
        if not user:
            return "User not found"

        is_correct = check_password_hash(user.password, credentials.password)
        if not is_correct:
            return "Bad password"


def get_user_service():
    return UserService(UserRepository())
