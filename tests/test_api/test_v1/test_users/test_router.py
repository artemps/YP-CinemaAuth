from typing import Callable

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient

from main import router
from repository.schemas import UserSchema, Roles
from api.v1.users.schemas import UserCreateIn, UserUpdateIn
from api.v1.auth.schemas import UserLoginIn
from services import UserService


async def test_register_new_user(client: AsyncClient, fake: Faker) -> None:
    user_in = UserCreateIn(email=fake.email(), password=fake.password())

    response = await client.post(url=router.url_path_for("register_user"), json=user_in.model_dump(exclude_unset=True))

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    assert user_in.email == body["email"]
    assert "id" in body
    assert "password" not in body


async def test_register_new_user_with_already_taken_email(client: AsyncClient, create_user: Callable) -> None:
    existing_user = await create_user()

    response = await client.post(
        url=router.url_path_for("register_user"),
        json=UserCreateIn(email=existing_user.email, password="12345678").model_dump(exclude_unset=True)
    )

    assert response.status_code == status.HTTP_409_CONFLICT


async def test_get_me(client: AsyncClient, authenticate_client: Callable, create_user: Callable) -> None:
    user = await create_user()
    client = await authenticate_client(client, user)

    response = await client.get(url=router.url_path_for("get_me"))

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert user.email == body["email"]
    assert user.first_name == body["first_name"]
    assert user.last_name == body["last_name"]
    assert str(user.id) == body["id"]


async def test_get_user(client: AsyncClient, authenticate_client: Callable, create_user: Callable) -> None:
    admin = await create_user(role=Roles.ADMIN)
    client = await authenticate_client(client, admin)

    response = await client.get(url=router.url_path_for("get_user", user_id=admin.id))

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert admin.email == body["email"]
    assert admin.first_name == body["first_name"]
    assert admin.last_name == body["last_name"]
    assert str(admin.id) == body["id"]


async def test_update_user(client: AsyncClient, authenticate_client: Callable, create_user: Callable) -> None:
    admin = await create_user(role=Roles.ADMIN)
    client = await authenticate_client(client, admin)
    user_in = UserUpdateIn(first_name="Test First Name", last_name="Test Last Name")

    response = await client.post(
        url=router.url_path_for("update_user", user_id=admin.id),
        json=user_in.model_dump(exclude_unset=True)
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert user_in.first_name == body["first_name"]
    assert user_in.last_name == body["last_name"]


async def test_show_user_login_history(client: AsyncClient, authenticate_client: Callable, create_user: Callable) -> None:
    admin = await create_user(role=Roles.ADMIN, password="12345678")
    client = await authenticate_client(client, admin)

    await client.post(
        url=router.url_path_for("login"),
        json=UserLoginIn(email=admin.email, password="12345678").model_dump()
    )

    response = await client.get(url=router.url_path_for("user_login_history", user_id=admin.id))

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert len(body) == 1
    assert body[0]["ip_address"]
    assert body[0]["user_agent"]
    assert body[0]["login_at"]


