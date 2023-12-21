from abc import ABC, abstractmethod
from uuid import UUID

from .schemas import UserSchema, UserLoginSchema, Roles, BaseUserSchema


class AbstractRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, data: dict) -> BaseUserSchema:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user_id: UUID, data: dict) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_id(self, user_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_user_role(self, user_id: UUID, role: Roles) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def remove_user_role(self, user_id: UUID, role: Roles) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_user_roles(self, user_id: UUID) -> list[Roles]:
        raise NotImplementedError

    @abstractmethod
    async def create_user_login_record(self, user_id: UUID, ip_address: str, user_agent: str) -> UserLoginSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_user_login_records(self, user_id: UUID, limit: int, offset: int) -> list[UserLoginSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_social_id(self, social_id: dict) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def create_user_social_account(self, user_id: UUID, social_info: dict):
        raise NotImplementedError
