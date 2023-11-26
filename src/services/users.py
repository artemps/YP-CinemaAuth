from unittest.mock import Mock, AsyncMock

from models import User


class UserService:
    db = {}

    async def get_user_by_login(self, login: str) -> User:

