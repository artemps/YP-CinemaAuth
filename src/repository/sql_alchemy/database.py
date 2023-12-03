import asyncio
from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from core.database import async_session
from repository.database import AbstractRepository
from repository.exceptions import ObjectAlreadyExists, ObjectDoesNotExist
from repository.schemas import UserSchema, UserLoginSchema, Roles
from .models import User, UserLogin, UserRole


class SQLAlchemyRepository(AbstractRepository):
    async def get_user_by_id(self, user_id: UUID) -> UserSchema:
        async with async_session() as session:
            statement = select(User).where(User.id == id)
            try:
                result = (await session.execute(statement)).scalar_one()
            except NoResultFound as error:
                raise ObjectDoesNotExist from error
            return UserSchema.model_validate(result, from_attributes=True)

    async def get_user_by_login(self, login: str) -> UserSchema:
        async with async_session() as session:
            statement = select(User).where(User.login == login)
            try:
                result = (await session.execute(statement)).scalar_one()
            except NoResultFound as error:
                raise ObjectDoesNotExist from error
            return UserSchema.model_validate(result, from_attributes=True)

    async def create_user(self, data: dict) -> UserSchema:
        async with async_session() as session:
            statement = insert(User).values(**data).returning(User)
            try:
                result = (await session.execute(statement)).scalar_one()
            except IntegrityError as error:
                raise ObjectAlreadyExists from error
            await session.commit()
            return UserSchema.model_validate(result, from_attributes=True)

    async def update_user(self, user_id: UUID, data: dict) -> UserSchema:
        async with async_session() as session:
            statement = update(User).where(User.id == id).values(**data).returning(User)
            try:
                result = (await session.execute(statement)).scalar_one()
            except IntegrityError as error:
                raise ObjectAlreadyExists from error
            await session.commit()
            return UserSchema.model_validate(result, from_attributes=True)

    async def delete_user_by_id(self, user_id: UUID) -> None:
        async with async_session() as session:
            try:
                user = session.get(User, user_id)
            except NoResultFound as error:
                raise ObjectDoesNotExist from error
            session.delete(user)
            await session.commit()

    async def set_user_role(self, user_id: int, role: Roles) -> UserSchema:
        async with async_session() as session:
            try:
                user, role = asyncio.gather(session.get(User, user_id), session.get(UserRole, role.value))
            except NoResultFound as error:
                raise ObjectDoesNotExist from error
            user.roles.add(role)
            await session.commit()
            return UserSchema.model_validate(user, from_attributes=True)

    async def remove_user_role(self, user_id: int, role: Roles) -> UserSchema:
        async with async_session() as session:
            try:
                user, role = asyncio.gather(session.get(User, user_id), session.get(UserRole, role.value))
            except NoResultFound as error:
                raise ObjectDoesNotExist from error
            user.roles.remove(role)
            await session.commit()
            return UserSchema.model_validate(user, from_attributes=True)

    async def create_user_login_record(self, user_id: UUID, ip_address: str, user_agent: str) -> UserLoginSchema:
        async with async_session() as session:
            record = UserLogin(user_id=user_id, ip_address=ip_address, user_agent=user_agent)
            session.add(record)
            await session.commit()
            return UserLoginSchema.model_validate(record, from_attributes=True)

    async def get_user_login_records(self, user_id: UUID, limit: int = 10, offset: int = 0) -> list[UserLoginSchema]:
        async with async_session() as session:
            statement = select(UserLogin).where(UserLogin.user_id == user_id).limit(limit).offset(offset).order_by(UserLogin.login_at.desc())
            result = (await session.execute(statement)).scalars()
            return [UserLoginSchema.model_validate(record, from_attributes=True) for record in result]
