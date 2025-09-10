from abc import ABC, abstractmethod
from contextlib import asynccontextmanager


class AbstractUnitOfWork(ABC):
    @asynccontextmanager
    @abstractmethod
    async def __call__(self):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
