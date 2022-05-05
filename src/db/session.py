from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings


def get_sync_db():
    engine = create_engine(f"postgresql://{settings.db_dsn}")
    Session = sessionmaker(engine, expire_on_commit=False)
    with Session() as db:
        return db
