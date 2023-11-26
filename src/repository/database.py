from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from sqlalchemy import insert, update, select

from models import User
from core.database import async_session


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def add_one(self, data: dict) -> UUID:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: UUID, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_by_login(self, login: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def check_unique_login(self, login: str) -> bool:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, data: dict) -> None:
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def update_one(self, id: UUID, data: dict):
        async with async_session() as session:
            stmt = update(self.model).where(self.model.id == id).values(**data)
            await session.execute(stmt)
            await session.commit()

    async def get_by_login(self, login: str) -> Optional[User]:
        async with async_session() as session:
            stmt = select(self.model).where(self.model.login == login)
            res = await session.execute(stmt)
            res = [x[0] for x in res]
            if not res:
                return None
            return res[0]

    async def check_unique_login(self, login: str) -> bool:
        async with async_session() as session:
            stmt = select(self.model).where(self.model.login == login)
            res = await session.execute(stmt)
            return len([x[0] for x in res]) > 0


class UserRepository(SQLAlchemyRepository):
    model = User
