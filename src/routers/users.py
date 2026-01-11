from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies import get_users_service
from src.schemas.users import UserBase
from src.services.users import UsersService

router = APIRouter(tags=["user"])


@router.get("/", response_model=list[UserBase])
async def get_users(
        users_service: Annotated[UsersService, Depends(get_users_service)],
):
    return await users_service.get_all()
