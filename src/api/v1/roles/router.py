from uuid import UUID

from fastapi import APIRouter, Depends, Body, Path, status
from fastapi.responses import JSONResponse

from api.dependencies import roles_required
from services import RoleService, get_role_service
from repository.schemas import Roles
from . import schemas
from .const import ENDPOINT_DESCRIPTIONS

router = APIRouter()


@router.post("/{user_id}", description=ENDPOINT_DESCRIPTIONS["set_role"])
@roles_required([Roles.ADMIN])
async def set_role(
    user_id: UUID = Path(..., description="User id"),
    role: schemas.RoleIn = Body(..., description="Role identifier"),
    role_service: RoleService = Depends(get_role_service),
) -> JSONResponse:
    await role_service.set(user_id, role.name)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Role {role.name} set for user {user_id}"})


@router.delete("/{user_id}", description=ENDPOINT_DESCRIPTIONS["delete_role"], status_code=status.HTTP_204_NO_CONTENT)
@roles_required([Roles.ADMIN])
async def delete_role(
    user_id: UUID = Path(..., description="User id"),
    role: schemas.RoleIn = Body(..., description="Role identifier"),
    role_service: RoleService = Depends(get_role_service),
) -> None:
    await role_service.remove(user_id, role.name)
