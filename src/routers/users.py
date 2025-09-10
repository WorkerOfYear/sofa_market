from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependencies.users import users_service
from src.schemas.users import UserCreateSchema, UserUpdateSchema, UserReadSchema
from src.services.users import UsersService

router = APIRouter(tags=["Users manage"])


@router.post("/", response_model=UserReadSchema)
async def add_user(
        user: UserCreateSchema,
        service: Annotated[UsersService, Depends(users_service)],
):
    return await service.add_user(user)


# @router.get("/")
# async def get_users(
#         service: Annotated[UsersService, Depends(users_service)],
# ) -> list[UserReadSchema]:
#     service.
#
#
#
# @router.get("/{user_id}")
# async def get_user(user_id: int):
#     ...
#
#
# @router.put("/{user_id}")
# async def update_user(user_id: int, user: UserUpdateSchema):
#     ...
#
#
# @router.delete("/{user_id}")
# async def delete_user(user_id: int):
#     ...
