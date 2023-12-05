from functools import wraps

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException, status

from repository.sql_alchemy.models import User
from repository.schemas import Roles
from services import (
    SecurityService,
    UserService,
    get_security_service,
    get_user_service,
)


async def authenticated_user(
    security_service: SecurityService = Depends(get_security_service),
    user_service: UserService = Depends(get_user_service),
    auth: AuthJWT = Depends(),
) -> User:
    await auth.jwt_required()
    login = await auth.get_jwt_subject()
    await security_service.authenticate(auth, login)
    user = await user_service.get(login=login)
    return user


def roles_required(roles_list: list[Roles]):
    def decorator(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            user_service = get_user_service()
            user = await user_service.get(id=kwargs.get("user_id"))
            if not set(roles_list).intersection(set([x.name for x in user.roles])):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
            return await function(*args, **kwargs)
        return wrapper
    return decorator
