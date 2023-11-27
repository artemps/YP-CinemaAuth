from fastapi import APIRouter, Depends

from services import SecurityService, UserService, get_user_service, get_security_service

from .const import ENDPOINT_DESCRIPTIONS
from . import schemas

from async_fastapi_jwt_auth import AuthJWT

router = APIRouter()


@router.post("/login", description=ENDPOINT_DESCRIPTIONS["/login"])
async def login(
    schema: schemas.UserLoginIn,
    security_service: SecurityService = Depends(get_security_service),
    user_service: UserService = Depends(get_user_service),
    Authorize: AuthJWT = Depends()
) -> schemas.UserLoginOut:
    user = await user_service.get(login=schema.login)
    security_service.verify_password(schema.password, user.password)
    access_token = await security_service.create_access_token(user.login, Authorize)
    refresh_token = await security_service.create_refresh_token(user.login, Authorize)
    return schemas.UserLoginOut(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh")
async def refresh(
        Authorize: AuthJWT = Depends(),
        security_service: SecurityService = Depends(get_security_service),
) -> schemas.UserLoginOut:

    new_tokens = await security_service.refresh_token(Authorize)
    return schemas.UserLoginOut(
        access_token=new_tokens.get("access_token"),
        refresh_token=new_tokens.get("refresh_token"),
        token_type="bearer"
    )
