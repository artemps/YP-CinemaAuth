from uuid import UUID

from fastapi import APIRouter, Depends, Body, Path, status
from fastapi.responses import JSONResponse

from services import UserService, get_user_service, RoleService, get_role_service
from . import schemas
from .const import ENDPOINT_DESCRIPTIONS

router = APIRouter()


@router.post("/{user_id}/roles", description=ENDPOINT_DESCRIPTIONS["set_role"])
async def set_role(
    user_id: UUID = Path(..., description="User id"),
    role: schemas.RoleIn = Body(..., description="Role identifier"),
    user_service: UserService = Depends(get_user_service),
    role_service: RoleService = Depends(get_role_service),
) -> JSONResponse:
    user = await user_service.get(id=user_id)
    await role_service.set_role(user, role)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Role {role} set for user {user.login}"})


@router.delete("/{user_id}/roles", description=ENDPOINT_DESCRIPTIONS["delete_role"])
async def delete_role(
    user_id: UUID = Path(..., description="User id"),
    role: schemas.RoleIn = Body(..., description="Role identifier"),
    user_service: UserService = Depends(get_user_service),
    role_service: RoleService = Depends(get_role_service),
) -> JSONResponse:
    user = await user_service.get(id=user_id)
    await role_service.delete_role(user, role)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
