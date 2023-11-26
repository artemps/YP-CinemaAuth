from fastapi import APIRouter, Depends, status

from api.dependencies import authenticated_user
from .const import ENDPOINT_DESCRIPTIONS
from . import schemas

router = APIRouter()


@router.post("/me", description=ENDPOINT_DESCRIPTIONS["/me"], status_code=status.HTTP_200_OK)
async def me(user=Depends(authenticated_user)) -> schemas.UserMeOut:
    return user

