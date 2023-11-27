from uuid import UUID

from fastapi import Depends

from services import UserService, SecurityService, get_user_service, get_security_service
from models import User


async def authenticated_user(
    token: str = Depends(SecurityService.auth_scheme),
    user_service: UserService = Depends(get_user_service),
    security_service: SecurityService = Depends(get_security_service),
) -> User:
    user_id = security_service.authenticate(token)
    user = await user_service.get(id=user_id)
    return user
