from abc import ABC, abstractmethod

from config import settings
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(
    settings.database_url,
    poolclass=pool.AsyncAdaptedQueuePool,
    pool_size=12,
    max_overflow=4,
    pool_pre_ping=True,
)

Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, entity):
        raise NotImplementedError

    @abstractmethod
    async def get(self, entity_id):
        raise NotImplementedError
