import typing
from abc import ABC, abstractmethod
from uuid import uuid4

from sqlalchemy import pool, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.repositories import models

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


class DocumentRepository(AbstractRepository):
    def __init__(self):
        self.session = Session()

    async def add(self, entity):
        async with self.session as session:
            async with session.begin():
                session.add(entity)

    async def get(self, id: uuid4) -> typing.Union[models.Document, None]:
        async with self.session as session:
            user = await session.get(models.Document, id)
            return user


class VaultRepository(AbstractRepository):
    def __init__(self):
        self.session = Session()

    async def add(self, entity):
        async with self.session as session:
            async with session.begin():
                session.add(entity)

    async def get(self, id: uuid4) -> typing.Union[models.Vault, None]:
        async with self.session as session:
            user = await session.get(models.Vault, id)
            return user

    async def get_vault_documents(
        self, id: uuid4
    ) -> typing.Optional[typing.List[models.Document]]:
        async with self.session as session:
            return await session.execute(
                select(models.Document).where(models.Document.vault_id == id)
            ).all()
