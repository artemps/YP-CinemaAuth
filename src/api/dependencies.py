from uuid import UUID

from fastapi import Depends, HTTPException, status

from services import UserService, SecurityService, get_user_service, get_security_service
from models import User

from async_fastapi_jwt_auth import AuthJWT

async def authenticated_user(
    id,
    token: str = Depends(SecurityService.auth_scheme),
    security_service: SecurityService = Depends(get_security_service),
    user_service: UserService = Depends(get_user_service),
    Authorize: AuthJWT = Depends()
) -> User:
    user = await user_service.get(id=id)
    user_id = await security_service.authenticate(Authorize, user.login)
    return user_id
