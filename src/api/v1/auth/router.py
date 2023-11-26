from fastapi import APIRouter, Depends

from services import SecurityService, UserService, get_user_service, get_security_service

from .const import ENDPOINT_DESCRIPTIONS
from . import schemas

router = APIRouter()


@router.post("/login", description=ENDPOINT_DESCRIPTIONS["/login"])
async def login(
    schema: schemas.UserLoginIn,
    security_service: SecurityService = Depends(get_security_service),
    user_service: UserService = Depends(get_user_service),
) -> schemas.UserLoginOut:
    user = await user_service.get(login=schema.login)
    security_service.verify_password(schema.password, user.password)
    access_token = security_service.create_access_token(user.id)
    return schemas.UserLoginOut(access_token=access_token, token_type="bearer")
