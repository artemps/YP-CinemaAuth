from uuid import UUID

from fastapi import APIRouter, Depends, status, Path, Body

from api.dependencies import authenticated_user
from services import get_security_service, SecurityService, UserService, get_user_service
from .const import ENDPOINT_DESCRIPTIONS
from . import schemas


router = APIRouter()


@router.post("/register", description=ENDPOINT_DESCRIPTIONS["register"], status_code=status.HTTP_201_CREATED)
async def register_user(
    schema: schemas.UserCreateIn = Body(..., description="User registration data"),
    user_service: UserService = Depends(get_user_service),
    security_service: SecurityService = Depends(get_security_service),
) -> schemas.UserOut:
    user = await user_service.create(schema, security_service)
    return user


@router.get("/{id}", description=ENDPOINT_DESCRIPTIONS["get_user"], dependencies=[Depends(authenticated_user)])
async def get_user(
    id: UUID = Path(..., description="User id"),
    user_service: UserService = Depends(get_user_service),
) -> schemas.UserOut:
    print(id)
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