from unittest.mock import patch

import pytest
from faker import Faker
from fastapi import status, FastAPI
from httpx import AsyncClient

from main import router
from api.v1.users.schemas import UserCreateIn
from api.v1.auth.schemas import UserLoginIn
from services import UserService, SecurityService


async def test_client_able_to_login(client: AsyncClient, fake: Faker, user_service: UserService) -> None:
    user_in = UserCreateIn(email=fake.email(), password=fake.password())
    await user_service.create(schema=user_in)
    credentials = UserLoginIn(email=user_in.email, password=user_in.password)

    response = await client.post(url=router.url_path_for("login"), json=credentials.model_dump())

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["access_token"]
    assert body["refresh_token"]
    assert body["token_type"] == "bearer"


async def test_client_can_not_login_with_wrong_password(client: AsyncClient, fake: Faker, user_service: UserService) -> None:
    user_in = UserCreateIn(email=fake.email(), password=fake.password())
    await user_service.create(schema=user_in)
    credentials = UserLoginIn(email=user_in.email, password=fake.password())

    response = await client.post(url=router.url_path_for("login"), json=credentials.model_dump())

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
