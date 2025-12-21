from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies.users import users_service
from src.schemas.users import BaseUser
from src.services.users import UsersService

router = APIRouter(tags=["user"])


@router.get("/")
async def get_users(
        user_service: Annotated[UsersService, Depends(users_service)],
) -> list[BaseUser]:
    return await user_service.get_users()
