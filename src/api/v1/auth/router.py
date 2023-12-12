import asyncio

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Request

from services import (
    SecurityService,
    UserService,
    get_security_service,
    get_user_service,
)
from . import schemas
from .const import ENDPOINT_DESCRIPTIONS

from core.settings_oauth import oauth
from core.limiter import limiter

from repository.exceptions import UserDoesNotExist, UserAlreadyExists
from api.v1.users.schemas import UserCreateIn


router = APIRouter()


@router.post("/login", description=ENDPOINT_DESCRIPTIONS["login"])
async def login(
        schema: schemas.UserLoginIn,
        request: Request,
        security_service: SecurityService = Depends(get_security_service),
        user_service: UserService = Depends(get_user_service),
        auth: AuthJWT = Depends()
) -> schemas.UserLoginOut:
    user = await user_service.get(email=schema.email)
    security_service.verify_password(schema.password, user.password)

    coro = user_service.create_login_record(
        user.id,
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.client.host,
    )
    asyncio.create_task(coro)
    access_token = await security_service.create_access_token(user.email, auth)
    refresh_token = await security_service.create_refresh_token(user.email, auth, access_token)

    return schemas.UserLoginOut(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh")
async def refresh(
        request: Request,
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
        request: Request,
        auth: AuthJWT = Depends(),
        security_service: SecurityService = Depends(get_security_service),
) -> schemas.UserLogout():
    await security_service.logout(auth)
    return schemas.UserLogout()


@router.get('/login-via-{social_network}')
async def login_via_social_network(
        request: Request,
        social_network
):
    redirect_uri = request.url_for(
        'social_network_callback',
        social_network=social_network)
    client = oauth.create_client(social_network)
    return await client.authorize_redirect(request, redirect_uri)


@router.get('/social-network-callback-{social_network}')
async def social_network_callback(
        request: Request,
        social_network,
        security_service: SecurityService = Depends(get_security_service),
        user_service: UserService = Depends(get_user_service),
        auth: AuthJWT = Depends()
):
    client = oauth.create_client(social_network)
    token = await client.authorize_access_token(request)

    social_network_response = await client.get('info', token=token)

    user_info = social_network_response.json()
    user = await user_service.user_via_social_network(user_info)

    coro = user_service.create_login_record(
        user.id,
        user_agent=request.headers.get("User-Agent"),
        ip_address=request.client.host,
    )
    asyncio.create_task(coro)
    access_token = await security_service.create_access_token(user.email, auth)
    refresh_token = await security_service.create_refresh_token(user.email, auth, access_token)

    return schemas.UserLoginOut(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
