from uuid import UUID

from fastapi import Depends
from sqlalchemy import insert, select, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.database import get_session, async_session
from repository.database import AbstractRepository
from repository.exceptions import RoleAlreadyExists, RoleDoesNotExist, UserDoesNotExist, UserAlreadyExists
from repository.schemas import UserSchema, UserLoginSchema, Roles, BaseUserSchema
from .models import User, UserLogin, UserRole


class SQLAlchemyRepository(AbstractRepository):
    async def get_user_by_id(self, user_id: UUID) -> UserSchema:
        async with get_session() as session:
            statement = select(User).where(User.id == user_id)
            try:
                result = (await session.execute(statement)).unique().scalar_one()
            except NoResultFound as error:
                raise UserDoesNotExist from error
            return UserSchema.model_validate(result, from_attributes=True)

    async def get_user_by_email(self, email: str) -> UserSchema:
        async with get_session() as session:
            statement = select(User).where(User.email == email)
            try:
                result = (await session.execute(statement)).unique().scalar_one()
            except NoResultFound as error:
                raise UserDoesNotExist from error
            return UserSchema.model_validate(result, from_attributes=True)

    async def create_user(self, data: dict) -> BaseUserSchema:
        async with get_session() as session:
            statement = insert(User).values(**data).returning(User)
            try:
                result = (await session.execute(statement)).unique().scalar_one()
            except IntegrityError as error:
                raise UserAlreadyExists from error
            await session.commit()
            return BaseUserSchema.model_validate(result, from_attributes=True)

    async def update_user(self, user_id: UUID, data: dict) -> UserSchema:
        async with get_session() as session:
            statement = update(User).where(User.id == user_id).values(**data)
            try:
                await session.execute(statement)
            except IntegrityError as error:
                raise UserAlreadyExists from error

            user = await session.get(User, user_id)
            await session.commit()
            return UserSchema.model_validate(user, from_attributes=True)

    async def delete_user_by_id(self, user_id: UUID) -> None:
        async with get_session() as session:
            try:
                user = session.get(User, user_id)
            except NoResultFound as error:
                raise UserDoesNotExist from error
            session.delete(user)
            await session.commit()

    async def set_user_role(self, user_id: int, role: Roles) -> UserSchema:
        async with get_session() as session:
            try:
                user = await session.get(User, user_id, options=[joinedload(User.roles)])
            except NoResultFound as error:
                raise UserDoesNotExist from error

            user_role = await self._get_or_create_role(session, role)
            if user_role in user.roles:
                raise RoleAlreadyExists

            user.roles.add(user_role)
            await session.commit()
            return UserSchema.model_validate(user, from_attributes=True)

    async def remove_user_role(self, user_id: int, role: Roles) -> UserSchema:
        async with get_session() as session:
            try:
                user = await session.get(User, user_id)
            except NoResultFound as error:
                raise UserDoesNotExist from error

            user_role = await self._get_or_create_role(session, role)
            try:
                user.roles.remove(user_role)
            except KeyError as error:
                raise RoleDoesNotExist from error

            await session.commit()
            return UserSchema.model_validate(user, from_attributes=True)

    async def _get_or_create_role(self, session: AsyncSession, role: Roles) -> UserRole:
        statement = select(UserRole).where(UserRole.name == role.value)
        try:
            role = (await session.execute(statement)).scalar_one()
        except NoResultFound:
            role = UserRole(name=role.value)
            session.add(role)
            await session.commit()
        return role

    async def get_user_roles(self, user_id: UUID) -> list[Roles]:
        async with get_session() as session:
            statement = select(User).where(User.id == user_id).options(joinedload(User.roles))
            try:
                user = (await session.execute(statement)).unique().scalar_one()
            except NoResultFound as error:
                raise UserDoesNotExist from error
            return [Roles(role.name) for role in user.roles]

    async def create_user_login_record(self, user_id: UUID, ip_address: str, user_agent: str) -> UserLoginSchema:
        async with get_session() as session:
            record = UserLogin(user_id=user_id, ip_address=ip_address, user_agent=user_agent)
            session.add(record)
            await session.commit()
            return UserLoginSchema.model_validate(record, from_attributes=True)

    async def get_user_login_records(self, user_id: UUID, limit: int = 10, offset: int = 0) -> list[UserLoginSchema]:
        async with get_session() as session:
            statement = select(UserLogin).where(UserLogin.user_id == user_id).limit(limit).offset(offset).order_by(UserLogin.login_at.desc())
            result = (await session.execute(statement)).scalars()
            return [UserLoginSchema.model_validate(record, from_attributes=True) for record in result]
