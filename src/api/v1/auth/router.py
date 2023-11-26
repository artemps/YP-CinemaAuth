from fastapi import APIRouter, Depends, HTTPException, status

from services import SecurityService, UserService

from .const import ENDPOINT_DESCRIPTIONS
from . import schemas

router = APIRouter()


@router.post("/register", description=ENDPOINT_DESCRIPTIONS["/register"], status_code=status.HTTP_201_CREATED)
async def register(
    schema: schemas.UserRegisterIn,
    user_service: UserService = Depends(),
) -> schemas.UserRegisterOut:
    user = await user_service.create_user(schema)
    return user


@router.post("/login", description=ENDPOINT_DESCRIPTIONS["/login"], status_code=status.HTTP_200_OK)
async def login(
    schema: schemas.UserLoginIn,
    security_service: SecurityService = Depends(),
    user_service: UserService = Depends(),
) -> schemas.UserLoginOut:
    user = await user_service.get_user_by_login(schema.login)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    is_verified = security_service.verify_password(schema.password, user.password)
    if not is_verified:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password")

    access_token = security_service.create_access_token(user.id)
    return schemas.UserLoginOut(access_token=access_token, token_type="bearer")
