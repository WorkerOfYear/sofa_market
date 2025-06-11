from src.database.models import User
from src.repositories.base import AbstractRepository
from src.schemas.users import UserCreateSchema, UserReadSchema


class UsersService:
    def __init__(self, users_repo: type[AbstractRepository[User]]):
        self.users_repo = users_repo()

    async def add_user(self, user: UserCreateSchema) -> UserReadSchema:
        user_dict = user.model_dump()
        user_dict["hashed_password"] = user_dict["password"]
        del user_dict["password"]
        new_user = await self.users_repo.add_one(user_dict)
        return new_user.to_read_model()

    async def get_all_users(self) -> list[UserReadSchema]:
        orm_users = await self.users_repo.find_all()
        return