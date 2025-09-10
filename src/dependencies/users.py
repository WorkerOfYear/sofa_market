from fastapi import Depends

from src.dependencies.uow import get_uow
from src.uow.sqlalchemy import UnitOfWork
from src.services.users import UsersService


def users_service(uow: UnitOfWork = Depends(get_uow)) -> UsersService:
    return UsersService(uow)
