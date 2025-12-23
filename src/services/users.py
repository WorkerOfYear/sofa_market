from src.uow.sqlalchemy import UnitOfWork
from src.database.models import User


class UsersService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_users(self) -> list[User]:
        return await self.uow.user_repo.get_all()
