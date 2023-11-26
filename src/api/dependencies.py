from fastapi import Depends, status, HTTPException

from services import UserService, SecurityService


async def authenticated_user(
    user_service: UserService = Depends(),
    token: str = Depends(SecurityService.authenticate),
) -> "UserModel":
    user = await user_service.get_user_by_id(token)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return user