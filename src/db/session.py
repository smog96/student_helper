from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.core.config import settings


def get_sync_db():
    engine = create_engine(f"postgresql://{settings.db_dsn}")
    Session = sessionmaker(engine, expire_on_commit=False)
    with Session() as db:
        return db


engine = create_async_engine(
    f"postgresql+asyncpg://{settings.db_dsn}", echo=True
)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_db():
    async with async_session() as db:
        yield db
