from uuid import UUID

from fastapi import Depends
from fastapi.routing import APIRouter

from schemas import UserCreate, UserLogin
from services.user import UserService, get_user_service

router = APIRouter(prefix="/users")


@router.post("")
async def add_user(
        user_create: UserCreate,
        user_service: UserService = Depends(get_user_service)
):
    status = await user_service.add_user(user_create)
    return {"status": status}


@router.post("/{user_id}")
async def edit_user(
        user_id: UUID,
        user_create: UserCreate,
        user_service: UserService = Depends(get_user_service)
):
    status = await user_service.edit_user(user_id, user_create)
    return {"status": status}


@router.post("/login")
async def make_login(
        credentials: UserLogin,
        user_service: UserService = Depends(get_user_service)
):
    status = await user_service.make_login(credentials)
    return {"status": status}
