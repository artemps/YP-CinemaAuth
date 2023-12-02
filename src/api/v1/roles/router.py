from uuid import UUID

from fastapi import APIRouter, Depends, Body, Path, status
from fastapi.responses import JSONResponse

from services import RoleService, get_role_service
from . import schemas
from .const import ENDPOINT_DESCRIPTIONS

router = APIRouter()


@router.post("/{user_id}/roles", description=ENDPOINT_DESCRIPTIONS["set_role"])
async def set_role(
    user_id: UUID = Path(..., description="User id"),
    role: schemas.RoleIn = Body(..., description="Role identifier"),
    role_service: RoleService = Depends(get_role_service),
) -> JSONResponse:
    await role_service.set_role(user_id, role.name)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Role {role.name} set for user {user_id}"})


@router.delete("/{user_id}/roles", description=ENDPOINT_DESCRIPTIONS["delete_role"])
async def delete_role(
    user_id: UUID = Path(..., description="User id"),
    role: schemas.RoleIn = Body(..., description="Role identifier"),
    role_service: RoleService = Depends(get_role_service),
) -> JSONResponse:
    await role_service.delete_role(user_id, role.name)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
