import asyncio

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends

from services import (
    SecurityService,
    UserService,
    get_security_service,
    get_user_service,
)
from . import schemas
from .const import ENDPOINT_DESCRIPTIONS

router = APIRouter()


@router.post("/login", description=ENDPOINT_DESCRIPTIONS["/login"])
async def login(
    schema: schemas.UserLoginIn,
    security_service: SecurityService = Depends(get_security_service),
    user_service: UserService = Depends(get_user_service),
    auth: AuthJWT = Depends()
):
    user = await user_service.get(email=schema.email)
    security_service.verify_password(schema.password, user.password)
    await user_service.make_email(user)
    access_token = await security_service.create_access_token(user.email, auth)
    refresh_token = await security_service.create_refresh_token(user.email, auth, access_token)
    return schemas.UserLoginOut(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh")
async def refresh(
    auth: AuthJWT = Depends(),
    security_service: SecurityService = Depends(get_security_service),
) -> schemas.UserLoginOut:
    new_tokens = await security_service.refresh_token(auth)
    return schemas.UserLoginOut(
        access_token=new_tokens.get("access_token"),
        refresh_token=new_tokens.get("refresh_token"),
        token_type="bearer",
    )


@router.post("/logout")
async def logout(
    auth: AuthJWT = Depends(),
    security_service: SecurityService = Depends(get_security_service),
) -> schemas.UserLogout():
    await security_service.logout(auth)
    return schemas.UserLogout()
