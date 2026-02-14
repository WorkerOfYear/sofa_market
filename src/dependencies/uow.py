from src.uow.sqlalchemy import UnitOfWork
from src.database.connection import async_session_maker


async def get_uow():
    async with UnitOfWork(async_session_maker)() as uow:
        yield uow
