from unittest.mock import Mock, AsyncMock


class UserService(Mock):
    get_user_by_login = AsyncMock()
    create_user = AsyncMock()