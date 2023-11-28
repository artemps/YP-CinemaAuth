from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import insert, select, update

from core.database import async_session
from models import User, UserLogin


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def add_one(self, data: dict) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: UUID, data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_login(self, login: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    async def check_unique_login(self, login: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def make_login(self, user: User) -> None:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> None:
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def update_one(self, id: UUID, data: dict) -> None:
        async with async_session() as session:
            stmt = update(self.model).where(self.model.id == id).values(**data)
            await session.execute(stmt)
            await session.commit()

    async def get_by_login(self, login: str) -> User:
        async with async_session() as session:
            stmt = select(self.model).where(self.model.login == login)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def get_by_id(self, id: UUID) -> User:
        async with async_session() as session:
            statement = select(self.model).where(self.model.id == id)
            result = await session.execute(statement)
            return result.scalar_one()

    async def check_unique_login(self, login: str) -> bool:
        async with async_session() as session:
            stmt = select(self.model).where(self.model.login == login)
            res = await session.execute(stmt)
            return len([x[0] for x in res]) > 0

    async def make_login(self, user: User) -> None:
        async with async_session() as session:
            stmt = insert(UserLogin).values({"user_id": user.id})
            await session.execute(stmt)
            await session.commit()


class UserRepository(SQLAlchemyRepository):
    model = User
