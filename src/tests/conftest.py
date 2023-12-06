import pytest

from api.v1.users.schemas import UserCreateIn, UserUpdateIn


@pytest.fixture
def test_user():
    return UserCreateIn(
        login="testuser",
        password="testpassword",
        first_name="create user",
        last_name="create user"
    )


@pytest.fixture
def test_user_update():
    return UserUpdateIn(
        first_name="updated user",
        last_name="updated user"
    )
