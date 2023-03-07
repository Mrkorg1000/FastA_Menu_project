from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from collections.abc import AsyncGenerator

# create engine for interaction with database
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)

# create async session for the interaction with database
async_session_maker = sessionmaker(bind=engine,
                                   class_=AsyncSession,
                                   expire_on_commit=False
)


async def get_session() -> AsyncGenerator: 
    async with async_session_maker() as session:
        yield session
        