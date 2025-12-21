from src.uow.sqlalchemy import UnitOfWork
from src.schemas.users import BaseUser


class UsersService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_users(self) -> list[BaseUser]:
        return list(await self.uow.user_repo.get_all())

