from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, status, Query

from api.dependencies import authenticated_user
from repository.sql_alchemy.models import User
from services import (
    SecurityService,
    UserService,
    get_security_service,
    get_user_service
)
from . import schemas
from .const import ENDPOINT_DESCRIPTIONS

router = APIRouter()


@router.post("/register", description=ENDPOINT_DESCRIPTIONS["register"], status_code=status.HTTP_201_CREATED)
async def register_user(
    schema: schemas.UserCreateIn = Body(..., description="User registration data"),
    user_service: UserService = Depends(get_user_service),
    security_service: SecurityService = Depends(get_security_service),
) -> schemas.UserOut:
    user = await user_service.create(schema, security_service)
    return user


@router.get("/me", description=ENDPOINT_DESCRIPTIONS["get_me"])
async def get_me(user: User = Depends(authenticated_user)) -> schemas.UserOut:
    return user


@router.get("/{id}", description=ENDPOINT_DESCRIPTIONS["get_user"], dependencies=[Depends(authenticated_user)])
async def get_user(
    id: UUID = Path(..., description="User id"),
    user_service: UserService = Depends(get_user_service),
) -> schemas.UserOut:
    user = await user_service.get(id=id)
    return user


@router.post("/{id}", description=ENDPOINT_DESCRIPTIONS["update_user"], dependencies=[Depends(authenticated_user)])
async def update_user(
    id: UUID = Path(..., description="User id"),
    schema: schemas.UserUpdateIn = Body(..., description="User update data"),
    user_service: UserService = Depends(get_user_service),
) -> schemas.UserOut:
    user = await user_service.update(id, schema)
    return user


@router.get("/{id}/login_history", description=ENDPOINT_DESCRIPTIONS["user_login_history"], dependencies=[Depends(authenticated_user)])
async def user_login_history(
    id: UUID = Path(..., description="User id"),
    limit: int = Query(10, description="Limit"),
    offset: int = Query(0, description="Offset"),
    user_service: UserService = Depends(get_user_service),
) -> list[schemas.UserLoginHistoryOut]:
    records = await user_service.get_login_records(id, limit, offset)
    return records