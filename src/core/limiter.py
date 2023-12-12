from slowapi import Limiter
from slowapi.util import get_ipaddr
from starlette.requests import Request
from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends

from core import settings
from repository.sql_alchemy.models import User


def get_token(request: Request) -> str:
    user = request.headers.get("Authorization")
    if user is None:
        user = get_ipaddr(request)
    return user


limiter = Limiter(
    key_func=get_token,
    storage_uri=f"redis://{settings.redis_host}:{settings.redis_port}/n",
    default_limits=[settings.limiter_default]
)
