from src.uow.sqlalchemy import UnitOfWork
from src.schemas.users import UserCreateSchema, UserReadSchema
from src.auth import hash_password


class UsersService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserCreateSchema) -> UserReadSchema:
        user_dict = user.model_dump()
        user_dict["hashed_password"] = hash_password(user_dict["password"])
        del user_dict["password"]
        new_user = await self.uow.user_repo.add(user_dict)
        return new_user.to_read_model()

    async def get_all_users(self) -> list[UserReadSchema]:
        orm_users = await self.users_repo.find_all()
        return