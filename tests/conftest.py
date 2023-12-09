import asyncio
from typing import Callable, Awaitable

import pytest
from async_fastapi_jwt_auth import AuthJWT
from fastapi import FastAPI
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from faker import Faker

from api.v1.users.schemas import UserCreateIn
from repository.schemas import UserSchema, Roles
from services import get_user_service, get_role_service, get_security_service, RoleService, SecurityService, UserService
from core.database import Base, metadata
from core import settings
from main import app


@pytest.fixture(scope="session")
def fake():
    return Faker()


@pytest.fixture(scope="session")
def event_loop() -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine(event_loop):
    engine = create_async_engine(settings.database_dsn, future=True, isolation_level="AUTOCOMMIT")
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        yield engine
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def fastapi_app(engine):
    yield app

    # cleanup
    async with engine.connect() as conn:
        query = text("TRUNCATE TABLE users_roles_map, users_logins, users, users_roles  RESTART IDENTITY CASCADE;")
        await conn.execute(query)


@pytest.fixture(scope="function")
def user_service() -> UserService:
    return get_user_service()


@pytest.fixture(scope="function")
def role_service() -> RoleService:
    return get_role_service()


@pytest.fixture(scope="function")
def security_service() -> SecurityService:
    return get_security_service()


@pytest.fixture(scope="function")
def auth_service() -> AuthJWT:
    return AuthJWT()


@pytest.fixture(scope="function")
async def client(fastapi_app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as client:
        yield client


@pytest.fixture(scope="function")
def create_user(user_service: UserService, role_service: RoleService, fake: Faker) -> Callable[[str, str, Roles], Awaitable[UserSchema]]:
    async def _create_user(email: str = None, password: str = None, role: Roles = None) -> UserSchema:
        user_in = UserCreateIn(email=email or fake.email(), password=password or fake.password())
        user = await user_service.create(schema=user_in)
        if role:
            await role_service.set(user.id, role)
        return user

    return _create_user


@pytest.fixture(scope="function")
def authenticate_client(
    security_service: SecurityService,
    auth_service: AuthJWT,
) -> Callable[[AsyncClient, UserSchema], Awaitable[AsyncClient]]:
    async def _authenticate_client(client: AsyncClient, user: UserSchema) -> AsyncClient:
        token = await security_service.create_access_token(user.email, auth_service)
        client.headers["Authorization"] = f"Bearer {token}"
        return client

    return _authenticate_client



# @pytest.fixture(scope="function")
# async def auth_user(fastapi_app, session):
#     user = await User.create(session, schema=UserCreate(username="testtest", password="testtest"))
#     token = create_access_token(user.id)
#     async with AsyncClient(app=fastapi_app, base_url=settings.server_address,
#                            headers={'Authorization': f'Bearer {token}'}) as client:
#         yield client, user