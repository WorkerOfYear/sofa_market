from asyncio import current_task
from typing import AsyncGenerator, Iterator

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from starlette.testclient import TestClient

import src.database.models
from src.config import settings
from src.database.connection import get_async_session
from src.database.db import Base
from src.main import app


admin_engine = create_async_engine(
    settings.DATABASE_URL, isolation_level="AUTOCOMMIT"
)
engine = create_async_engine(
    settings.TEST_DATABASE_URL, echo=False, connect_args={"timeout": 0.5}
)


async def create_test_database():
    """Create the test database if it doesn't exist."""
    async with admin_engine.connect() as conn:
        try:
            await conn.execute(
                text(f"CREATE DATABASE {settings.POSTGRES_TEST_DB_NAME}")
            )
        except ProgrammingError:
            print("Database already exists, continuing...")


@pytest.fixture(scope="session", autouse=True)
async def async_db_connection() -> AsyncGenerator[AsyncConnection, None]:
    """
    Create the test database schema before any tests run,
    and drop it after all tests are done.
    """
    await create_test_database()

    async with engine.begin() as conn:
        # separate connection because .create_all makes .commit inside
        await conn.run_sync(Base.metadata.create_all)

    conn = await engine.connect()
    try:
        yield conn
    except:
        raise
    finally:
        await conn.rollback()
        await conn.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


async def _session_within_transaction(
        async_db_conn: AsyncConnection
) -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = async_sessionmaker(
        bind=async_db_conn,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    transaction = await async_db_conn.begin()

    yield async_scoped_session(async_session_maker, scopefunc=current_task)

    # no need to truncate, all data will be rolled back
    await transaction.rollback()


@pytest.fixture(scope="function")
async def async_db_session(
        async_db_connection: AsyncConnection
) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a new database session for each test and roll it back after the test.
    """
    async for session in _session_within_transaction(async_db_connection):
        # setup some data per function
        yield session


@pytest.fixture(scope="function")
async def client(db: AsyncSession) -> AsyncGenerator[TestClient, None]:
    """
    Provide a TestClient that uses the test database session.
    Override the get_async_session dependency to use the test session.
    """

    def override_get_db() -> Iterator[AsyncSession]:
        yield db

    app.dependency_overrides[get_async_session] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
async def inspect_list_tables() -> list[str]:
    """Provide a list with table names which exist in test db"""

    def use_inspector(connection: AsyncConnection) -> list[str]:
        inspector = inspect(connection)
        return inspector.get_table_names()

    async with engine.begin() as conn:
        return await conn.run_sync(use_inspector)



